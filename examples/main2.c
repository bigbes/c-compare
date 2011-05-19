void bubblesort(int a[], int n){
    int i, j, k;
    for(i=0; i < n; ++i){
        for (j = i+1; j<n; ++j)
            if (a[i] < a[j])
                k = a[i];
                a[i] = a[j];
                a[j] = k;
    }
}

int main(){
    int a[] = {9,8,7,6,5,4,3,2,1,0};
    bubblesort(a, 10);
    return 0;
}