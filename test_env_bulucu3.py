import yaml

def validate_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        print("YAML dosyası geçerli.")
    except yaml.YAMLError as e:
        print(f"YAML dosyası hatası: {e}")
    except FileNotFoundError:
        print("Dosya bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

validate_yaml('your_yaml_file.yaml')