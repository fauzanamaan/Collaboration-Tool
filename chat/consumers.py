# Importing necessary libraries and modules
import json  # Used for working with JSON data
from datetime import datetime  # Used for working with dates and times
from django.db import connection  # Used for interacting with the database
# Used for encrypting and decrypting messages
from .encryption import VernamCipher
# Used for interacting with User data
from django.contrib.auth.models import User
# Base class for WebSocket consumers
from channels.generic.websocket import AsyncWebsocketConsumer
# Used for running synchronous functions in an asynchronous manner
from asgiref.sync import sync_to_async
# Importing the models from the application
from .models import Department, Region, MessageDepartment, MessageRegion

# Consumer for handling WebSocket connections related to departments


class DepartmentConsumer(AsyncWebsocketConsumer):
    # Function to handle new WebSocket connections
    async def connect(self):
        # Get the department name from the URL route
        self.department_name = self.scope['url_route']['kwargs']['department_name']
        self.department_group_name = 'chat_%s' % self.department_name

        # Add the consumer to the department group
        await self.channel_layer.group_add(
            self.department_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    # Function to handle WebSocket disconnections
    async def disconnect(self, close_code):
        # Remove the consumer from the department group
        await self.channel_layer.group_discard(
            self.department_group_name,
            self.channel_name
        )

    # Function to handle incoming messages from the WebSocket
    async def receive(self, text_data):
        # Parse the received JSON data
        data = json.loads(text_data)

        # Extract the message, username, and department from the data
        message = data['message']
        username = data['username']
        department = data['department']

        # Save the message to the database
        encrypted_message, key = await self.save_message(username, department, message)

        # Send the message to the department group
        await self.channel_layer.group_send(
            self.department_group_name,
            {
                'type': 'chat_message',
                'message': encrypted_message,
                'username': username,
                'key': key
            }
        )

    # Function to handle incoming messages from the department group
    async def chat_message(self, event):
        encrypted_message = event['message']
        key = event['key']
        username = event['username']
        decrypted_message = VernamCipher.decrypt(encrypted_message, key)

        # Send decrypted message to WebSocket
        await self.send(text_data=json.dumps({
            'message': decrypted_message,
            'username': username
        }))

    # Function to save a message to the database
    @sync_to_async
    def save_message(self, username, department, message):
        # Function to get the user and department objects from the database
        def get_user_and_department(username, department_slug):
            # Use raw SQL queries to retrieve user and department objects
            users = User.objects.raw(
                'SELECT * FROM auth_user WHERE username = %s', [username])
            departments = Department.objects.raw(
                'SELECT * FROM chat_department WHERE slug = %s', [department_slug])

            # Check if the user and department exist
            if len(users) > 0 and len(departments) > 0:
                return users[0], departments[0]
            else:
                # Raise an error if the user or department does not exist
                if len(users) == 0:
                    raise User.DoesNotExist(
                        "User matching query does not exist.")
                if len(departments) == 0:
                    raise Department.DoesNotExist(
                        "Department matching query does not exist.")
        user, department = get_user_and_department(username, department)

        # Generate a key for encryption
        key = VernamCipher.key_generator(message)

        # Encrypt the message using VernamCipher
        encrypted_message = VernamCipher.encrypt(message, key)

        # Function to create a new MessageDepartment object in the database
        def create_message_department(user, department, encrypted_message, key):
            current_date_time = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO chat_messagedepartment (user_id, department_id, content, key, date_added)
                    VALUES (%s, %s, %s, %s, %s)
                """, [user.id, department.id, encrypted_message, key, current_date_time])
        create_message_department(user, department, encrypted_message, key)
        return encrypted_message, key

# The RegionConsumer class is similar to the DepartmentConsumer class, but it handles WebSocket connections related to regions instead of departments.


# Consumer for handling WebSocket connections related to regions
class RegionConsumer(AsyncWebsocketConsumer):
    # This function is called when the WebSocket is handshaking as part of the connection process.
    async def connect(self):
        # Get the region name from the URL route
        self.region_name = self.scope['url_route']['kwargs']['region_name']
        self.region_group_name = 'chat_%s' % self.region_name

        # Add the consumer to the region group
        await self.channel_layer.group_add(
            self.region_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    # This function is called when the WebSocket closes for any reason.
    async def disconnect(self, close_code):
        # Remove the consumer from the region group
        await self.channel_layer.group_discard(
            self.region_group_name,
            self.channel_name
        )

    # This function is called when the server receives a message from WebSocket
    async def receive(self, text_data):
        # Parse the received JSON data
        data = json.loads(text_data)
        print(data)

        # Extract the message, username, and region from the data
        message = data['message']
        username = data['username']
        region = data['region']

        # Save the message to the database
        encrypted_message, key = await self.save_message(username, region, message)

        # Send the message to the region group
        await self.channel_layer.group_send(
            self.region_group_name,
            {
                'type': 'chat_message',
                'message': encrypted_message,
                'username': username,
                'key': key
            }
        )

    # This function is called when the server receives a message from region group
    async def chat_message(self, event):
        encrypted_message = event['message']
        key = event['key']
        username = event['username']
        decrypted_message = VernamCipher.decrypt(encrypted_message, key)

        # Send decrypted message to WebSocket
        await self.send(text_data=json.dumps({
            'message': decrypted_message,
            'username': username
        }))

    # This function is used to save the message to the database
    @sync_to_async
    def save_message(self, username, region, message):

        def get_user_and_region(username, region_slug):
            # Use raw SQL queries to retrieve user and region objects
            users = User.objects.raw(
                'SELECT * FROM auth_user WHERE username = %s', [username])
            regions = Region.objects.raw(
                'SELECT * FROM chat_region WHERE slug = %s', [region_slug])

            if len(users) > 0 and len(regions) > 0:
                return users[0], regions[0]
            else:
                if len(users) == 0:
                    raise User.DoesNotExist(
                        "User matching query does not exist.")
                if len(regions) == 0:
                    raise Region.DoesNotExist(
                        "Region matching query does not exist.")
        user, region = get_user_and_region(username, region)

        # Generate a key for encryption
        key = VernamCipher.key_generator(message)

        # Encrypt the message using VernamCipher
        encrypted_message = VernamCipher.encrypt(message, key)

        # Create a new MessageRegion object with the user, region, encrypted message, and key
        def create_message_region(user, region, encrypted_message, key):
            current_date_time = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO chat_messageregion (user_id, region_id, content, key, date_Added)
                    VALUES (%s, %s, %s, %s, %s)
                """, [user.id, region.id, encrypted_message, key, current_date_time])
        create_message_region(user, region, encrypted_message, key)
        return encrypted_message, key
