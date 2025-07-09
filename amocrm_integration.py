#!/usr/bin/env python3
"""
Простая интеграция с amoCRM API для проверки подключения
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class AmoCRMClient:
    """Простой клиент для работы с amoCRM API"""
    
    def __init__(self):
        load_dotenv()
        self.domain = os.getenv('AMOCRM_DOMAIN')
        self.client_id = os.getenv('AMOCRM_CLIENT_ID')
        self.client_secret = os.getenv('AMOCRM_CLIENT_SECRET')
        self.redirect_uri = os.getenv('AMOCRM_REDIRECT_URI')
        self.access_token = os.getenv('AMOCRM_ACCESS_TOKEN')
        
        if not all([self.domain, self.client_id, self.client_secret]):
            raise ValueError("Не все обязательные переменные окружения установлены")
        
        self.base_url = f"https://{self.domain}"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}' if self.access_token else None
        }
    
    def get_auth_url(self) -> str:
        """Получить URL для авторизации"""
        return (f"{self.base_url}/oauth2/access_token?"
                f"client_id={self.client_id}&"
                f"response_type=code&"
                f"redirect_uri={self.redirect_uri}")
    
    def get_token_by_code(self, code: str) -> Dict[str, Any]:
        """Получить токен по коду авторизации"""
        url = f"{self.base_url}/oauth2/access_token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Токен получен успешно!")
            print(f"Access Token: {token_data.get('access_token')}")
            print(f"Refresh Token: {token_data.get('refresh_token')}")
            return token_data
        else:
            print(f"❌ Ошибка получения токена: {response.status_code}")
            print(response.text)
            return {}
    
    def test_connection(self) -> bool:
        """Проверить подключение к API"""
        if not self.access_token:
            print("❌ Access token не установлен")
            return False
        
        url = f"{self.base_url}/api/v4/account"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                account_info = response.json()
                print("✅ Подключение к amoCRM успешно!")
                print(f"Аккаунт: {account_info.get('name', 'N/A')}")
                print(f"ID: {account_info.get('id', 'N/A')}")
                print(f"Поддомен: {account_info.get('subdomain', 'N/A')}")
                return True
            else:
                print(f"❌ Ошибка подключения: {response.status_code}")
                print(response.text)
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса: {e}")
            return False
    
    def get_contacts(self, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Получить список контактов (простой тест API)"""
        if not self.access_token:
            print("❌ Access token не установлен")
            return None
        
        url = f"{self.base_url}/api/v4/contacts"
        params = {"limit": limit}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                contacts = response.json()
                print(f"✅ Получено контактов: {len(contacts.get('_embedded', {}).get('contacts', []))}")
                return contacts
            else:
                print(f"❌ Ошибка получения контактов: {response.status_code}")
                print(response.text)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса: {e}")
            return None

def main():
    """Основная функция для тестирования интеграции"""
    print("🚀 Тестирование интеграции с amoCRM")
    print("=" * 50)
    
    try:
        client = AmoCRMClient()
        
        # Если нет access token, покажем URL для авторизации
        if not client.access_token:
            print("📋 Для работы с API нужен access token.")
            print("Откройте этот URL в браузере для авторизации:")
            print(client.get_auth_url())
            print("\nПосле авторизации скопируйте код из URL и введите его:")
            code = input("Введите код авторизации: ").strip()
            
            if code:
                token_data = client.get_token_by_code(code)
                if token_data.get('access_token'):
                    print("\n💡 Добавьте этот токен в файл .env:")
                    print(f"AMOCRM_ACCESS_TOKEN={token_data['access_token']}")
                    return
        else:
            # Тестируем подключение
            if client.test_connection():
                print("\n📞 Тестируем получение контактов...")
                contacts = client.get_contacts()
                
                if contacts:
                    contacts_list = contacts.get('_embedded', {}).get('contacts', [])
                    if contacts_list:
                        print("\n📋 Первые контакты:")
                        for i, contact in enumerate(contacts_list[:3], 1):
                            name = contact.get('name', 'Без имени')
                            contact_id = contact.get('id', 'N/A')
                            print(f"  {i}. {name} (ID: {contact_id})")
                    else:
                        print("📭 Контактов пока нет")
        
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        print("\n💡 Создайте файл .env на основе .env.example")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()