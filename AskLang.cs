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
        public string use_tesser = "";

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

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void button5_Click(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void button1_Click_1(object sender, EventArgs e)
        {

        }

        private void button2_Click_1(object sender, EventArgs e)
        {

        }

        private void button5_Click_1(object sender, EventArgs e)
        {

        }

        private void button4_Click_1(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click_2(object sender, EventArgs e)
        {
            foreach (RadioButton rb1 in LangBox.Controls)
            {
                if (rb1.Checked)
                {
                    language = rb1.Text.ToLower();
                    break;
                }
            }

            foreach (RadioButton rb2 in TesserBox.Controls)
            {
                if (rb2.Checked)
                {
                    use_tesser = rb2.Text.ToLower();
                    break;
                }
            }
            Close();
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }
    }
}
