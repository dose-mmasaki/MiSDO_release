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
    public partial class PasswordForm : Form
    {
        public PasswordForm()
        {
            InitializeComponent();
        }

        public bool check;

        private void PasswordForm_Load(object sender, EventArgs e)
        {

        }


       

        public bool CheckPass()
        {
            if (textBoxPass.Text == "admin" != true)
            {
                MessageBox.Show("パスワードが間違っています。", "確認",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }
            Close();
            return true;
        }

        private void buttonOK_Click_1(object sender, EventArgs e)
        {
            check = CheckPass();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            // form2を閉じる
            Close();
            return;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void contextMenuStrip1_Opening(object sender, CancelEventArgs e)
        {

        }

        private void textBoxPass_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
