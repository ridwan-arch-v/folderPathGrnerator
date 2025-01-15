import os
from colorama import Fore, Back, Style, init

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

class ProjectStructure:
    def __init__(self):
        self.structure = []
        self.current_path = []  # Menyimpan folder/folder yang sedang aktif

    def add_folder(self, folder_name):
        """ Menambahkan folder ke struktur """
        # Menambahkan folder ke struktur dengan path yang benar
        folder_path = os.path.join(*self.current_path, folder_name)
        self.structure.append(folder_path)
        print(f'{Fore.GREEN}{Back.BLACK}{Style.BRIGHT}MEMBUAT FOLDER COMAND = {{fl}}{folder_path} 📁')

    def add_file(self, file_name):
        """ Menambahkan file ke struktur """
        # Menambahkan file ke dalam folder yang benar
        file_path = os.path.join(*self.current_path, file_name)
        self.structure.append(file_path)
        print(f'{Fore.GREEN}{Back.BLACK}{Style.BRIGHT}MEMBUAT FILE COMAND = {{f}}{file_path} 📄')

    def display_structure(self):
        """ Menampilkan struktur dengan format garis vertikal dan sambungan """
        print("\nStruktur Project:")
        for item in self.structure:
            indent_level = item.count(os.sep)  # Menghitung level indentasi berdasarkan folder
            folder_or_file = item.replace(os.sep, '---').strip()

            # Menampilkan folder/file dengan emoji
            if '.' in folder_or_file:
                print(' ' * indent_level * 2 + f'  ├── {folder_or_file} 📄')
            else:
                print(' ' * indent_level * 2 + f'  ├── {folder_or_file} 📁')

    def generate_commands(self):
        """ Menghasilkan perintah CMD atau terminal untuk membuat folder/file """
        commands = []
        current_folder = ""

        for item in self.structure:
            # Jika item berakhiran '.', buat file dengan perintah `touch`
            if '.' in item:
                command = f'touch {item}'
            else:
                command = f'mkdir -p {item}'
            
            commands.append(command)

        return commands

    def navigate_folder(self, folder_name):
        """ Masuk ke folder dan tampilkan pesan """
        self.current_path.append(folder_name)
        print(f'\n{Fore.YELLOW}{Back.BLACK}MASUK KE FOLDER COMAND = {{fl-in}}{folder_name}')
        print(f'Anda berada di dalam folder: {"/".join(self.current_path)}')

    def exit_folder(self):
        """ Keluar dari folder dan tampilkan pesan """
        if self.current_path:
            self.current_path.pop()
            print(f'\n{Fore.RED}{Back.BLACK}KELUAR DARI FOLDER COMAND = {{fl-out}}')
            print(f'Anda berada di dalam folder: {"/".join(self.current_path) if self.current_path else "root"}')
        else:
            print(f'{Fore.RED}Anda sudah berada di root folder, tidak bisa keluar lagi.')

# Fungsi untuk menangani input struktur
def create_structure():
    project = ProjectStructure()
    
    print(f'{Fore.CYAN}{Style.BRIGHT}Masukkan folder/file, tekan Enter untuk folder/file yang sama.')
    print(f'{Fore.CYAN}{Style.BRIGHT}Gunakan {{fl-in}}nama-folder untuk masuk ke folder.')
    print(f'{Fore.CYAN}{Style.BRIGHT}Gunakan {{fl-out}} untuk keluar dari folder.')
    print(f'{Fore.CYAN}{Style.BRIGHT}Gunakan {{f}}nama-file.jenis untuk membuat file.')
    print(f'{Fore.CYAN}{Style.BRIGHT}Ketik "done" untuk selesai.\n')
    
    while True:
        # Input untuk folder/file dengan indentasi
        item = input("Masukkan perintah: ").strip()
        
        if item.lower() == 'done':
            break
        
        if item.lower().startswith('{fl-in}'):
            folder_name = item[len('{fl-in}'):].strip()
            project.navigate_folder(folder_name)
        elif item.lower().startswith('{fl-out}'):
            project.exit_folder()
        elif item.lower().startswith('{fl}'):
            folder_name = item[len('{fl}'):].strip()
            project.add_folder(folder_name)
        elif item.lower().startswith('{f}'):
            file_name = item[len('{f}'):].strip()
            project.add_file(file_name)
        else:
            print(f'{Fore.RED}Perintah tidak dikenali. Coba lagi.')

    print("\nStruktur Project:")
    project.display_structure()

    print("\nPerintah CMD/Powershell:")
    commands = project.generate_commands()
    for command in commands:
        print(f'{Fore.YELLOW}{Style.BRIGHT}{command}')

if __name__ == '__main__':
    create_structure()
