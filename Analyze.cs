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
using System.Windows.Forms.DataVisualization.Charting;
//using System.Windows.Media;

namespace DoNuTS_dotNET4_0
{
    public partial class Analyze : Form
    {
        public Analyze()
        {
            InitializeComponent();
        }

        // DBへのパス
        //string db_file = @".\Resources\DONUTS.db";
        //string db_file = @".\Resources\DONUTS.db";


        // チェックボックスから代入するリスト
        public List<string> modality_list = new List<string>();

        string py37 = "py -3.7";


        string selected_column  = "";
        private void chart1_Click(object sender, EventArgs e)
        {

        }

        private void Analyze_Load(object sender, EventArgs e)
        {

        }

        



        private void button1_Click(object sender, EventArgs e)
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

                string modality = "(" + s + ")";
                string target = selected_column;

                string str_to_analyze = @".\Resources\analyze.py";



                Process p = new Process();
                ProcessStartInfo info = new ProcessStartInfo();
                info.FileName = "cmd.exe";
                info.RedirectStandardInput = true;
                info.UseShellExecute = false;

                p.StartInfo = info;
                p.Start();

                string args = " --target " + target + " --modality " + modality;

                string startanalyze = "call " + py37 + " " + str_to_analyze + args;

                using (StreamWriter sw = p.StandardInput)
                {
                    sw.WriteLine("call .\\donuts_env\\Scripts\\activate");
                    sw.WriteLine(startanalyze);
                }
                p.WaitForExit();


                //loadSQLite(sql);
                //using (SQLiteConnection conn = new SQLiteConnection("Data Source=" + db_file))

                //{
                //    DataTable dataTable = new DataTable();

                //    conn.Open();

                //    // data格納インスタンス
                //    var adapter = new SQLiteDataAdapter(sql, conn);
                //    // DataTable作成
                //    DataTable dataTable1 = new DataTable();
                //    // Dataset作成
                //    DataSet dataSet = new DataSet();

                //    // データ取得
                //    adapter.Fill(dataTable1);


                //    var list1 = dataTable1.AsEnumerable().ToList<DataRow>();
                //    List<double> list2 = new List<double>();

                //    for (int i = 0; i < list1.Count; i++)
                //    {
                //        try
                //        {
                //            list2.Add(double.Parse(list1[i].ItemArray[0].ToString()));
                //        }
                //        catch
                //        {
                //            // 何もしない
                //        }
                //    }

                //    chart1.Series.Clear();
                //    chart1.ChartAreas.Clear();
                //    string chart_area = selected_column;
                //    try
                //    {
                //        chart1.ChartAreas.Add(new ChartArea(chart_area));
                //    }
                //    catch
                //    {
                //        // ignore
                //    }

                //    chart1.ChartAreas[0].AxisX.IsMarginVisible = false;
                //    //chart1.Size = new Size(400, 300);


                //    string legend1 = selected_column;
                //    chart1.Series.Add(legend1);

                //    chart1.Series[legend1].ChartType = SeriesChartType.BoxPlot;




                //    chart1.Series[legend1].Points.Add(list2.ToArray());
                //    chart1.Series[legend1]["BoxPlotWhiskerPercentile"] = "true";
                //    chart1.Series[legend1]["DrawingStyle"] = "Wedge";
                //    //Color color = new System.Drawing.Color();
                //    //color = Color.Blue;
                //    //chart1.Series[legend1].Color = color;

                //    //chart1.Series[legend1].set

                //}
           
            }
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            selected_column = radioButton1.Text;
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            selected_column = radioButton2.Text;
        }

        private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}
