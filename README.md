# How to run Razor

sudo docker pull chenxiong/razor:0.04
sudo docker run --rm -it chenxiong/razor:0.04

1. Run and trace the binary with inputs under train : 
```
python run_razor.py train
```
2. Debloat the binary without applying heuristics
```
python run_razor.py debloat
```
3. Check if the debloated program passes the tests:
```
python run_razor.py test | grep "Floating"
```
4. Apply heuristic zCode:
```
python run_razor.py extend_debloat 1
```
5. Apply heuristic zCall:
```
python run_razor.py extend_debloat 2
```
6. Apply heuristic zLib:
```
python run_razor.py extend_debloat 3
```
7. Apply heuristic zFunc:
```
python run_razor.py extend_debloat 4
```
