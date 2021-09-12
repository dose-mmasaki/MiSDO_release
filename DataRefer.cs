using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using System.Data.Odbc;
using System.Data.SQLite;
using System.Data.SQLite.Linq;
using System.Diagnostics;

namespace DoNuTS_dotNET4_0
{
    public partial class DataRefer : Form
    {
        public DataRefer()
        {
            InitializeComponent();
        }

        
        string sql = "";

        // DBへのパス
        string db_file = @".\Resources\DONUTS.db";

        // 選択された tabel
        string select_table = "";

        // チェックボックスから代入するリスト
        public List<string> modality_list = new List<string>();

        // 検索欄で使用する
        string search_column = "";
        string search_text = "";

        string py37 = "py -3.7";
        string LOWPATH = "";

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void title_Click(object sender, EventArgs e)
        {

        }


        // Sqliteからデータを読み込む
        private void load_and_show_SQLite(string sql)
        {
            using (SQLiteConnection conn = new SQLiteConnection("Data Source=" + db_file))

            {
                DataTable dataTable = new DataTable();

                conn.Open();

                //var sql = "SELECT * FROM " + select_table;
                var adapter = new SQLiteDataAdapter(sql, conn);
                adapter.Fill(dataTable);

                // データを表示
                dataGridView1.DataSource = dataTable;
                //dataGridView1.AutoResizeColumns();
            }
        }


        // パスワードを入力するformを表示
        private void PasswordForm()
        {
            // Display the password form.
            PasswordForm frm = new PasswordForm();
            frm.ShowDialog();
            if (frm.check == true)
            {
                using (SQLiteConnection conn = new SQLiteConnection("Data Source=" + db_file))
                {

                    string query = "SELECT * FROM " + select_table;

                    SQLiteDataAdapter adapter = new SQLiteDataAdapter();
                    adapter.TableMappings.Add(db_file, select_table);
                    adapter.SelectCommand = new SQLiteCommand(query, conn);

                    SQLiteCommandBuilder commandBuilder = new SQLiteCommandBuilder(adapter);
                    adapter.UpdateCommand = commandBuilder.GetUpdateCommand();
                    Console.WriteLine(adapter.UpdateCommand.CommandText);

                    adapter.Update((DataTable)dataGridView1.DataSource);
                    MessageBox.Show("更新完了");
                }
            }
            else
            {
                MessageBox.Show("変更がキャンセルされました.");
            }
        }


        private void button3_Click(object sender, EventArgs e)
        {
            sql = "SELECT * FROM " + select_table;
            try
            {
                // DBを読み込み，表示
                load_and_show_SQLite(sql);
            }
            catch
            {
                MessageBox.Show("データが存在しません.", "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            select_table = comboBox1.SelectedItem.ToString();
        }

        

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            search_column = comboBox2.Text;
        }

        private void button6_Click(object sender, EventArgs e)
        {
            modality_list.Clear();
            string s = "";
            if (checkedListBox1.CheckedItems.Count != 0)
            {

                for (int x = 0; x < checkedListBox1.CheckedItems.Count; x++)
                {
                    modality_list.Add(checkedListBox1.CheckedItems[x].ToString());
                    //s = s + "Checked Item" + (x + 1).ToString() + " = " + checkedListBox1.CheckedItems[x].ToString() + "\n";
                }

                for (int i = 0; i < modality_list.Count; i++)
                {
                    if (i == modality_list.Count - 1)
                    {
                        s = s + "'" + modality_list[i].ToString() + "'";
                    }
                    else
                    {
                        s = s + "'" + modality_list[i].ToString() + "'" + ",";
                    }
                }

                s = "(" + s + ")";
                sql = "SELECT * FROM ALL_DATA " +
                    "WHERE Identified_Modality in " + s +
                    " AND " + search_column + " LIKE " + "'%" + search_text + "%'";

                load_and_show_SQLite(sql);
            }




            //string sql = "SELECT * FROM Auto WHERE " + search_column + " LIKE " + "'%" + search_text + "%'";
            //loadSQLite(sql);
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            search_text = textBox1.Text;
        }

        private void button5_Click(object sender, EventArgs e)
        {
            PasswordForm();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string str_to_out_csv = @".\Resources\out_csv.py";

            try
            {
                sql = "--sql \"" + sql + "\"";
                string start_out_csv = "call " + py37 + " " + str_to_out_csv + " " + sql;

                Process p = new Process();
                ProcessStartInfo info = new ProcessStartInfo();
                info.FileName = "cmd.exe";
                info.RedirectStandardInput = true;
                info.UseShellExecute = false;

                p.StartInfo = info;
                p.Start();

                using (StreamWriter sw = p.StandardInput)
                {
                    sw.WriteLine("call .\\donuts_env\\Scripts\\activate");
                    sw.WriteLine(start_out_csv);
                }
                p.WaitForExit();
            }
            catch
            {
                MessageBox.Show("出力できません.\n取得または検索からデータを表示させた後に再度試してください.", "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
        }

        private void button8_Click(object sender, EventArgs e)
        {
            using (var reader = new StreamReader(@".\Resources\Path_excel.txt"))
            {
                string excel_path = reader.ReadToEnd();
                //excel_path = "--path \"" + excel_path + "\"";


                try
                {
                    System.Diagnostics.Process p =
                        System.Diagnostics.Process.Start(excel_path, @".\Resources\latest.csv");
                    //System.Diagnostics.Process.Start(@".\Resources\openexcel.exe",  excel_path);

                }
                catch
                {
                    MessageBox.Show("Excelを開けません.\nファイル→設定→PathからPathを変更してください.", "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                }
            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Analyze analyze = new Analyze();
            analyze.Show();
        }

        private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }


        /// <summary>

        /// フォルダ内の最新datファイルのファイル名を取得します。

        /// </summary>

        /// <param name="folderName">フォルダ名を指定します。</param>

        /// <returns>最新datファイルのファイル名を返します。</returns>
        public string getNewestFileName(string folderName, string extension)
        {
            string[] files = System.IO.Directory.GetFiles(folderName, extension, System.IO.SearchOption.TopDirectoryOnly);
            string newestFileName = string.Empty;

            System.DateTime updateTime = System.DateTime.MinValue;

            foreach (string file in files)
            {

                // それぞれのファイルの更新日付を取得する

                System.IO.FileInfo fi = new System.IO.FileInfo(file);

                // 更新日付が最新なら更新日付とファイル名を保存する

                if (fi.LastWriteTime > updateTime)

                {

                    updateTime = fi.LastWriteTime;

                    newestFileName = file;

                }
            }
            // ファイル名を返す
            return System.IO.Path.GetFileName(newestFileName);
        }



        private void button2_Click(object sender, EventArgs e)
        {
            if (LOWPATH == "")
            {
                MessageBox.Show("Path を入力してください");
            }
            else
            {
                string str_to_show = @".\Resources\show_low_data.py";
                string dicomtxt = getNewestFileName(@".\Resources\temp", "*.txt");
                string pix = getNewestFileName(@".\Resources\temp", "*.png");

                try
                {
                    // 前回までのファイルを削除
                    FileInfo fileinfo_txt = new FileInfo(dicomtxt);
                    fileinfo_txt.Delete();
                }
                catch
                {

                }
                try
                {
                    // 前回までのファイルを削除
                    FileInfo fileInfo_pic = new FileInfo(pix);
                    fileInfo_pic.Delete();
                }
                catch
                {

                }


                string arg = "--path \"" + LOWPATH + "\"";
                string start_show = "call " + py37 + " " + str_to_show + " " + arg;


                Process p = new Process();
                ProcessStartInfo info = new ProcessStartInfo();
                info.FileName = "cmd.exe";
                info.RedirectStandardInput = true;
                info.UseShellExecute = false;

                p.StartInfo = info;
                p.Start();

                using (StreamWriter sw = p.StandardInput)
                {
                    sw.WriteLine("call .\\donuts_env\\Scripts\\activate");
                    sw.WriteLine(start_show);
                }
                p.WaitForExit();


                if (File.Exists(dicomtxt))
                {

                    // 画像を表示する
                    Dicomtxt dicomtxtform = new Dicomtxt();
                    dicomtxtform.Show();
                }
                else
                {

                }


                if (File.Exists(pix))
                {

                    // 画像を表示する
                    Picture picture = new Picture();
                    picture.Show();
                }
                else
                {

                }

            }
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            LOWPATH = textBox2.Text;
        }

        private void DataRefer_Load(object sender, EventArgs e)
        {

        }

        private void button7_Click(object sender, EventArgs e)
        {

        }
    }
}
