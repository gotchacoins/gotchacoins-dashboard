import os


def delete_migrations(base_path: str = ".") -> None:
    """
    Django 프로젝트 루트에서 각 앱의 `migrations` 폴더 내 *_initial.py 파일을 삭제합니다.
    """
    for app in os.listdir(base_path):
        app_path = os.path.join(base_path, app)
        migrations_path = os.path.join(app_path, "migrations")

        if os.path.isdir(migrations_path):
            for filename in os.listdir(migrations_path):
                if filename.endswith(".py") and filename != "__init__.py":
                    file_path = os.path.join(migrations_path, filename)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        else:
            # migrations 폴더가 없는 경우
            continue


def run() -> None:
    delete_migrations()
