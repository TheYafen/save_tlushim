#!/mnt/c/TheYafen/scripts/save_tlushim/.venv/bin/python
import get_payslips
import save_gdrive

def main():
    files_names_list = get_payslips.get_latest_payslip()
    print(f"Files to upload from main: {files_names_list}")
    save_gdrive.save_to_gdrive(files_names_list)

if __name__ == "__main__":
    main()