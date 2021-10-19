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
    public partial class AskModality : Form
    {
        public AskModality()
        {
            InitializeComponent();
        }

        public string modality = "";

        private void button3_Click(object sender, EventArgs e)
        {
            Close();
            return;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            modality = button1.Text;
            Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            modality = button2.Text;
            Close();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            modality = button4.Text;
            Close();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            modality = button5.Text;
            Close();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            modality = button6.Text;
            Close();
        }
    }
}
