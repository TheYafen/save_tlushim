<<<<<<< HEAD
#!/mnt/c/my_scripts/jopa/.venv/bin/python
import get_payslips
import save_gdrive

def main():
    files_names_list = get_payslips.get_latest_payslip()
    print(f"Files to upload from main: {files_names_list}")
    save_gdrive.save_to_gdrive(files_names_list)
=======
#!/mnt/c/TheYafen/scripts/save_tlushim/.venv/bin/python
import get_payslips
#import save_gdrive

def main():
    files_names_list = get_payslips.get_latest_payslip()
    # Couldn't make upload to gdrive work, so I commented it out for now. Will try again later.
    #save_gdrive.save_to_gdrive()
>>>>>>> 9796c69 (from home)

if __name__ == "__main__":
    main()