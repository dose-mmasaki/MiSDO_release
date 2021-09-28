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
    public partial class AskLang : Form
    {
        public AskLang()
        {
            InitializeComponent();
        }
        public string language = "";

        private void label1_Click(object sender, EventArgs e)
        {

        }

 

        private void button1_Click(object sender, EventArgs e)
        {
            language = "jpn";
            Close();
        }
    

        private void button2_Click(object sender, EventArgs e)
        {
            language = "eng";
            Close();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Close();
            return;
        }

    }
}
