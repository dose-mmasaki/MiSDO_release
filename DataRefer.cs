using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Data.SQLite;
using System.Data.SQLite.Linq;

namespace DoNuTS_dotNET4_0
{
    public partial class DataRefer : Form
    {
        public DataRefer()
        {
            InitializeComponent();
        }

        // DBへのパス
        string db_file = @".\Resources\DONUTS.db";
        string select_table = "";
        private void button2_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection("Data Source=" + db_file))
            {
                try
                {
                    conn.Open();
                    MessageBox.Show("Connection Success", "Connection Message", MessageBoxButtons.OK, MessageBoxIcon.Information);

                }
                catch (Exception exception)
                {
                    MessageBox.Show(exception.Message, "Connection Message", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection("Data Source=" + db_file))
            {
                var dataTable = new DataTable();

                try
                {
                    var sql = "SELECT * FROM " + select_table;
                    var adapter = new SQLiteDataAdapter(sql, conn);
                    adapter.Fill(dataTable);
                    dataGridView1.DataSource = dataTable;
                }
                catch
                {
                    MessageBox.Show("Select Modality", "SELECT ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string str_to_out_csv = @".\Resources\out_csv.exe";

            var proc = new System.Diagnostics.Process();
            proc.StartInfo.FileName = str_to_out_csv;
            proc.Start();
            proc.WaitForExit();
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            select_table = comboBox1.SelectedItem.ToString();
        }
    }
}
