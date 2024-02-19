from src.user_interaction import user_interaction
from src.utils import load_data_database


def main():
    """
    Основная функция по работе с программой.
    """
    print("Возможно придется подождать, так как вакансий не мало.")
    load_data_database()
    user_interaction()


if __name__ == "__main__":
    main()
