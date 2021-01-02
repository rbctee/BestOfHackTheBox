# Only Real Life Boxes Script

## What

This is a simple script that I use to download data from HackTheBox' API, which I use to generate an HTML table containing various information, e.g. Machine name, Difficulty, and more importantly the matrix. The latter contains 5 scores (from 0 to 10):

- Enumeration
- Real-Life
- CVE
- Custom Exploitation
- CTF-like

![Example of the output](./images/example.png)

## Why

At the time of writing, I didn't know any other method to get the information I needed.

## How

The script it's not very user-friendly: you have to:

- add your own `API_KEY` (either inside `main.py` or in a new file `secrets.py`)
- create the foldr `data/` (used to write `.csv` and `.json` files)
- change the functions called inside the `main`

```py
if __name__ == "__main__":
    write_data_all_machines()
    write_data_all_matrices()
    write_matrices_data_to_csv()
    write_matrices_data_to_csv(maker_or_aggregate='maker')
```

First you have to download data from the API, and then write this data to file, which in turn is used to generate two `CSV` files.

After you get the aforementioned files, you can use the package [csvtotable](https://github.com/vividvilla/csvtotable) to generate the HTML files.