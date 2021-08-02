using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace DoNuTS_dotNET4_0
{
    public partial class Menu : Form
    {
        public Menu()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string str_to_donuts = @".\Resources\main.exe";

            var proc = new System.Diagnostics.Process();
            proc.StartInfo.FileName = str_to_donuts;
            proc.Start();
            proc.WaitForExit();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            var DR = new DataRefer();
            DR.Show();
        }
    }
}
