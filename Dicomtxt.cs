using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace DoNuTS_dotNET4_0
{
    public partial class Dicomtxt : Form
    {
        public Dicomtxt()
        {
            InitializeComponent();
        }
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

        private void Dicomtxt_Load(object sender, EventArgs e)
        {
            string dir = @".\Resources\temp\";
            string path = getNewestFileName(dir, "*.txt");
            path = dir + path;
            using (var reader = new StreamReader(path))
            {
                textBox1.Text = reader.ReadToEnd();
            }
        }
    }
}
