player1_num_list = list(input("自分の数値を入力してください"))
player2_num_list = list(input("自分の数値を入力してください"))
digit = 3

def game(player,prediction):
    eats = 0
    bites = 0

    for i in range(digit):
        prediction_num = prediction[i]
        print(prediction_num)
        if player[i] == prediction_num:
            eats = eats + 1
        
        if any(prediction_num  in player[j] for j in range(digit)):
            bites = bites + 1

    return str(eats) + "EAT" + str(bites-eats) + "BITE"

player = 1

while True:
    
    if player % 2 == 1:
        input_prediction = list(input("予測値を入力してください（player1）"))
        ans = game(player2_num_list, input_prediction)
        print(ans)
        if ans == "3EAT0BITE":
            print("player1の勝利です")
            break
        
    if player % 2 == 0:
        input_prediction = list(input("予測値を入れてください（player2）"))
        ans = game(player1_num_list, input_prediction)
        print(ans)
        if ans == "3EAT0BITE":
            print("player2の勝利です")
            break
    player = player + 1



  

    


    
        


        

        

        
        

