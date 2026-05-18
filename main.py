import get_payslips

SAVE_DIR = "Payslips"

def main():
    get_payslips.get_latest_payslip(SAVE_DIR)

if __name__ == "__main__":
    main()