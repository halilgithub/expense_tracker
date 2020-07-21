# expense_tracker
I developed a sample **Expense Tracker** with Python and PyQt5 library.

| **Expense Tracker Panel:** |
|:----:|
| ![Expense Tracker Panel1](https://github.com/halilgithub/expense_tracker/blob/master/screen_shots/mainwindow_empty.png "Expense Tracker Panel1") |

## introduction and status

It simply tracks personal expenses & deposits each as a list item 
and within a nice visual printout.
After adding or removing an item, the balance is updated automatically.
Trashing the printout and start from scratch is possible.
Saving the printout in a text file is possible.

Tested in Ubuntu 20.4 and Windows 10 successfully.

## features

Basically you can:
  + add expense & deposit
  + remove expense & deposit
  + trash printout
  + save printout in a txt file

## usage

Execute the program from command line:

```console
foo@bar:~$ python main.py
```

Start to fillout a printout. You should enter an amount and description
then add it as an expense item or deposit item. 
When removing an item, select the item in the list and press the 'Remove Item' button.
The buttons for saving and trashing the printout are on the menubar.

| **sample Printout:** |
|:----:|
| ![Expense Tracker Panel2](https://github.com/halilgithub/expense_tracker/blob/master/screen_shots/mainwindow_entries.png "Expense Tracker Panel2") |

## copyright and license
This project is under the MIT License.
