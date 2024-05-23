from piccolo.apps.migrations.auto.migration_manager import MigrationManager

from piccolo_db.tables import Device, Users


ID = "2024-05-22T00:49:11:291219"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    async def run():
        data = [{'name': 'Трансформатор 1', 'type': 'трансформатор', 'is_active': True, 'status': 'исправен'},
                {'name': 'Трансформатор 2', 'type': 'трансформатор', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Трансформатор 3', 'type': 'трансформатор', 'is_active': True, 'status': 'исправен'},  
                {'name': 'Трансформатор 4', 'type': 'трансформатор', 'is_active': True, 'status': 'исправен'},
                {'name': 'Разъединитель 1_1', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'},
                {'name': 'Разъединитель 1_2', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'},
                {'name': 'Разъединитель 1_3', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'},
                {'name': 'Разъединитель 1_4', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_1', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_2', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_3', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_4', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_5', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_6', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_7', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 2_8', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_1', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_2', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_3', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_4', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_5', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_6', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_7', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_8', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_9', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_10', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_11', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_12', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_13', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_14', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_15', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 3_16', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 4_1', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 4_2', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 4_3', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 4_4', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}, 
                {'name': 'Разъединитель 4_5', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'},
                {'name': 'Разъединитель 4_6', 'type': 'разъединитель', 'is_active': True, 'status': 'исправен'}]
        for i in data:
            await Device(**i).save()

        admin_user = {'email': 'admin@admin.com', 'name': 'Главный администратор', 'role': 'admin', 'hashed_password': '$2b$12$p2uvNBYxb0MNBKlk6XK6W.4oDULDbkyhHpOOWOJNYc4I8bRfkW0OO'}
        await Users(**admin_user).save()

    manager.add_raw(run)

    return manager

