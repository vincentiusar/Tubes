#include <bits/stdc++.h> 

using namespace std;

void printArray(int arr[], int n) { 
    for (int i = 0; i < n; i++) 
        cout << arr[i] << " "; 
    cout << "\n"; 
} 

void inputArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
}

void oddEvenSort(int arr[], int n) { 
    /*
    I.S. element di dalam array belum terurut dari kecil 
    ke besar (masih random)
    F.S. element di dalam array sudah terurut dari kecil 
    ke besar
    */

    int total = 0, iterasi = 1; 
    
    // total = penghitung jumlah pertukaran
    // iterasi = prenghitung banyaknya perulangan
    
    bool isSorted = false;
    /* variable boolen menyatakan array sudah terurut atau
    belum
    */

    int banding = 0; //menghitung banyaknya operasi perbandingan

    while (!isSorted) { 
        isSorted = true;    // mengasumsikan array sudah terurut
        int count = 0;      // count = penghitung pertukaran tiap 1 iterasi
        
        // Perform Bubble sort untuk index ganjil 
        for (int i = 1; i <= n - 2; i = i + 2) { 
            banding++;
            if (arr[i] > arr[i+1]) {    //perbandingan index array dengan index selanjutnya
                swap(arr[i], arr[i+1]); 
                isSorted = false;   //jika pertukaran terjadi, maka array belum terurut
                count++; total++;  
            }
        }
        // Perform Bubble sort untuk index genap 
        for (int i = 0; i <= n - 2; i = i + 2) { 
            banding++;
            if (arr[i] > arr[i+1]) {    //perbandingan index array dengan index selanjutnya
                swap(arr[i], arr[i+1]); 
                isSorted = false;   //jika pertukaran terjadi, maka array belum terurut
                count++; total++;
            } 
        }
        cout << iterasi++ << "  |  " << count << "  |  " << total << "  |  " << banding << "  |  ";
        printArray(arr, n);
    }
    cout << endl << "banding = " << banding << endl;
} 

int main() { 
    int n; cout << "Masukkan jumlah angka : "; cin >> n;
    int arr[n];
    
    cout << "input sebanyak " << n << " angka : ";
    inputArray(arr, n);
    cout << "Iterasi | Jumlah Tukar | Total Pertukaran | Jumlah Banding | Array" << endl;
    oddEvenSort(arr, n);
    cout << endl << "Hasil Akhir = ";
    printArray(arr, n); 
} 