#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "Windows.h"
#include "fstream"
#include "stdlib.h"
#include "string"
#include <QFileDialog>

int co=0;
int no_of_frames;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_2_clicked()
{
    std::string s1,s2;
    std::string lS1;
    s1="Normal";
    s2="Comic";
    lS1=ui->label_5->text().toStdString();
    if(lS1==s1)
        lS1=s2;
    else
        lS1=s1;
    ui->label_5->setText(QString::fromStdString(lS1));

}

void MainWindow::on_pushButton_clicked()
{
    std::string s[5];
    std::string lS1;
    lS1=ui->label_4->text().toStdString();
    s[0]="English";
    s[1]="French";
    s[2]="German";
    s[3]="Italian";
    s[4]="Spanish";
    int f=0;
    for(int i=0;i<5;i++)
        if(s[i]==lS1)
            f=i;
    f=(f+1)%5;
    lS1=s[f];
    ui->label_4->setText(QString::fromStdString(lS1));

}

void MainWindow::on_pushButton_6_clicked()
{
    std::string s;
    s=ui->lineEdit_2->text().toStdString();
    ui->lineEdit_2->setText(QString::fromStdString(""));
    ui->label_7->setText(QString::fromStdString(s));
}

void MainWindow::on_pushButton_4_clicked()
{
    
    system("mkdir \"C:/Users/DM/Documents/Vook\"");
    system("mkdir \"C:/Users/DM/Documents/Vook/frames\"");
    system("mkdir \"C:/Users/DM/Documents/Vook/result\"");
    std::ofstream fout;
    std::ifstream fin;
    std::string s;
    s=ui->lineEdit->text().toStdString();
    fout.open("C:/Users/DM/Documents/Vook/info.txt");
    fout<<s<<std::endl;
    s=ui->label_4->text().toStdString();
    fout<<s<<std::endl;
    s=ui->label_5->text().toStdString();
    fout<<s<<std::endl;
    fout.close();
    fout.open("C:/Users/DM/Documents/Vook/status.txt");
    fout<<0;
    fout.close();

    fin.open("C:/Users/DM/Documents/Vook/status.txt");
    int n=0;

    system("python C:/Users/DM/Desktop/Vook/Vook/scripts/import.py");

    while(n==0)
    {
        Sleep(5000);
        fin>>n;
        fin.seekg(0);
    }
    fin.close();

    //Logic to read the caption
    fin.open("C:/Users/DM/Documents/Vook/output.txt");
    getline(fin,s);
    ui->textEdit->setText(QString::fromStdString(s));
    fin.close();

    //Logic for initial image
    fin.open("C:/Users/DM/Documents/Vook/frame_count.txt");
    fin>>no_of_frames;
    fin.close();
    QPixmap mypix("C:/Users/DM/Documents/Vook/frames/0.jpg");
    ui->label_11->setPixmap(mypix);
    QPixmap mypix1("C:/Users/DM/Documents/Vook/frames/1.jpg");
    ui->label_10->setPixmap(mypix1);
    QPixmap mypix2("C:/Users/DM/Documents/Vook/frames/2.jpg");
    ui->label_9->setPixmap(mypix2);
    QPixmap mypix3("C:/Users/DM/Documents/Vook/frames/3.jpg");
    ui->label_8->setPixmap(mypix3);


}


void MainWindow::on_pushButton_3_clicked()
{
    system("python C:/Users/DM/Desktop/Vook/Vook/scripts/export.py");
}

void MainWindow::on_pushButton_7_clicked()
{
    std::string s1,s2,s3,s4;
    if(co<no_of_frames-4)
    {
        co++;
        s1=s2=s3=s4="C:/Users/DM/Documents/Vook/frames/";

        s1+=std::to_string(co);
        s1+=".jpg";
        s2+=std::to_string(co+1);
        s2+=".jpg";
        s3+=std::to_string(co+2);
        s3+=".jpg";
        s4+=std::to_string(co+3);
        s4+=".jpg";

        //ui->label_7->setText(QString::fromStdString(s1));
        QPixmap mypix(s1.c_str());
        ui->label_11->setPixmap(mypix);
        QPixmap mypix1(s2.c_str());
        ui->label_10->setPixmap(mypix1);
        QPixmap mypix2(s3.c_str());
        ui->label_9->setPixmap(mypix2);
        QPixmap mypix3(s4.c_str());
        ui->label_8->setPixmap(mypix3);
    }

}

void MainWindow::on_pushButton_8_clicked()
{
    std::string s="C:/Users/DM/Documents/Vook/frames/";
    s+=std::to_string(co);
    s+=".jpg";
    QPixmap mypix(s.c_str());
    ui->label_6->setPixmap(mypix);
}

void MainWindow::on_pushButton_5_clicked()
{
    std::ofstream fo;
    fo.open("C:/Users/DM/Documents/Vook/img.txt", std::ios_base::app);
    fo<<co<<std::endl;
    fo.close();
    fo.open("C:/Users/DM/Documents/Vook/caption.txt", std::ios_base::app);
    std::string s=ui->label_7->text().toStdString();
    fo<<s<<std::endl;
    fo.close();
}

void MainWindow::on_pushButton_9_clicked()
{
    QString filepath=QFileDialog::getOpenFileName(
                this,
                tr("Select the Video File"),
                "C://",
                "All Files (*.*);;Video File (*.mp4)"       //Only two typpes of files allowed that is all files and video type
                );
    ui->lineEdit->setText(filepath);
}

void MainWindow::on_pushButton_10_clicked()
{
    system("rmdir C:\\Users\\DM\\Documents\\Vook /Q /S");
}
