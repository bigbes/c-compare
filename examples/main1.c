typedef struct{
    int a;
    int b;
    double c;
} olo;

typedef struct {
    olo a;
    double f;
} _C;

void bubblesort(int a[], int n){
    int k,b,c;
    for(k=0; k < n; ++k){
        for (b = k+1; b<n; ++b)
            if (a[k] < a[b])
                c = a[k];
                a[k] = a[b];
                a[b] = c;
    }
}

int main(){
    int zx[] = {9,8,7,6,5,4,3,2,1,0};
    bubblesort(zx, 10);
    _C ololo;
    return 0;
}
