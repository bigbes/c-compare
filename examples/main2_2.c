int main(){
  for (int i = 0; i < 100; ++i)
    for (int j = 0; j < 100; ++j){
      if (j == 50) return j;
    }
}