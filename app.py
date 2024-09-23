import os
import json
import subprocess
import webbrowser

config_file_path = 'config.json'

def create_config():
    project_file_path = input("C++のプロジェクトファイルの場所を入力してください。おそらく通常であればCドライブ直下においておくように指示があったと思います。:")

    config = {
        "project_file_path": project_file_path
    }
    if not (os.path.exists(project_file_path) and os.path.isdir(project_file_path)):
        print("指定されたプロジェクトファイルの場所が存在しないか、ディレクトリではありません。")
        exit(1)
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

    return config

def load_config():
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    return config

if __name__ == "__main__":
    include_path = os.environ.get('INCLUDE', '')
    if "C:\\Program Files (x86)\\Windows Kits\\" not in include_path:
        print("このプログラムは、Visual Studio 2022 Developer Command Promptから起動してください。プログラムを終了します。")
        input("Enterを押してください。")
        exit(1)
    os.environ.copy()
    if not os.path.exists(config_file_path):
        print("config.jsonファイルが存在しません。新しいファイルを作成します。")
        config = create_config()
    else:
        config = load_config()
    try:
        number = input("今回の演習の番号を入力してください: ")
        project_file_path = config['project_file_path']
        if os.path.exists(project_file_path) and os.path.isdir(project_file_path):
            folders = os.listdir(project_file_path)
            error = 0
            matching_folders = [folder for folder in folders if os.path.isdir(os.path.join(project_file_path, folder)) and folder.startswith(number)]
            print("コンパイルを開始します。これには時間がかかります。")
            for folder in matching_folders:
                folder_path = os.path.join(project_file_path, folder)
                if os.path.exists(folder_path + '\\' + folder + ".exe"):
                    os.remove(folder_path + '\\' + folder + ".exe")
                    os.remove(folder_path + '\\' + folder + ".obj")
                print(f"{folder}", end='...')
                result = subprocess.run('nmake report', cwd=folder_path, shell=True, capture_output=True, text=True)
                if not "この実行結果はそれぞれのフォルダのresult.txtに保存されています" in result.stdout:
                    print("失敗")
                    print("")
                    print("**************************************************")
                    print(result.stdout)
                    print("**************************************************")
                    print("")
                    error = 1
                else:
                    print("成功")
            if(error == 1):
                print("コンパイルに失敗した課題があります。ご確認ください。", end='')
                exit(1)
            print("レポートを生成します...")
            bb_result = subprocess.run('bb.bat', cwd=folder_path, shell=True, capture_output=True, text=True)
            print("レポートを生成しました。")
            new = 1
            for folder in matching_folders:
                print(project_file_path + r'\report-' + folder + '.html')
                url = project_file_path + r'\report-' + folder + '.html'
                webbrowser.open(url, new=new, autoraise=True)
                new = 2
            print("**************************************************")
            print("必ず成否を確認の上、提出してください。")
            print("**************************************************")

        else:
            print("指定されたプロジェクトファイルの場所が存在しません。")
    except ValueError:
        print("有効な数字を入力してください。")