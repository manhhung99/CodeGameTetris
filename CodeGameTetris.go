package main
import(
	"fmt"
	"math/rand"
	// "reflect"
	// "os"
	// "strings"
)
var ListBlock=[][][]int{
	[][]int{
		[]int{1,1,1},
		[]int{1,0,0},
		[]int{0,0,0},
	},
	[][]int{
		[]int{1,1,1},
		[]int{0,0,1},
		[]int{0,0,0},
	},
	[][]int{
		[]int{1,1,1},
		[]int{0,1,0},
		[]int{0,0,0},
	},
	[][]int{
		[]int{1,1,0},
		[]int{0,1,1},
		[]int{0,0,0},
	},
	[][]int{
		[]int{0,1,1},
		[]int{1,1,0},
		[]int{0,0,0},
	},
	[][]int{
		[]int{0,0,0,0},
		[]int{1,1,1,1},
		[]int{0,0,0,0},
		[]int{0,0,0,0},
	},
	[][]int{
		[]int{1,1},
		[]int{1,1},
	},
}
var Color=[]string {
    "\033[0;31;41m $\033[0m",    //Text: Red, Background: Red
    "\033[0;32;42m $\033[0m",    //Text: Green, Background: Green
    "\033[0;33;43m $\033[0m",    //Text: Yellow, Background: Yellow
    "\033[0;34;44m $\033[0m",    //Text: Blue, Background: Blue
    "\033[0;35;45m $\033[0m",    //Text: Purple, Background: Purple
    "\033[0;36;46m $\033[0m",    //Text: Cyan, Background: Cyan
    "\033[0;37;47m $\033[0m",    //Text: White, Background: White
}


// create screen contain block
func InitScreen(row int,colum int)[][]int{
	RowScreen:=make([]int,colum)
	Screen:=make([][]int,row)
	for Row:=0;Row<row;Row++{
		Screen[Row]=RowScreen
		// fmt.Println(Screen[Row])
	}
	return Screen
}


// random to choice block appear
func RandomBlock(ListBlock [][][]int)([][]int,[]int){
	Coordinate:=[]int{0,3}
	NumberBlock:=rand.Intn(7)
	NewBlock:=ListBlock[NumberBlock]
	Number:=rand.Intn(7)+1
	for row:=0;row<len(NewBlock);row++{
		for colum:=0;colum<len(NewBlock[row]);colum++{
			if NewBlock[row][colum]!=0{
				NewBlock[row][colum]=Number
			}
		}
	}
	return NewBlock,Coordinate
}

// 
func CopyBlock(Block [][]int)[][]int{
	NewBlock:=make([][]int,len(Block))
	// fmt.Println(NewBlock)
	for row:=range Block{
		NewBlock[row]=make([]int,len(Block[row]))
	}
	for row:=range Block{
		for colum:=range Block[row]{
			NewBlock[row][colum]=Block[row][colum]
		}
	}
	return NewBlock
}


func TestBlockNext(MainScreen [][]int,NextScreen [][]int)bool{
	LinhCanh:=0
	for row:=range MainScreen{
		for colum:=range MainScreen[row]{
			if NextScreen[row][colum]!=0{
				if MainScreen[row][colum]!=0{
					LinhCanh=1
				}
			}
		}
	}
	if LinhCanh==0{
		return false
	}else{
		return true
	}
}


// 
func CopyCoordinate(Coordinate []int)[]int{
	NewCoordinate:=make([]int,len(Coordinate))
	for i:=range Coordinate{
		NewCoordinate[i]=Coordinate[i]
	}
	return NewCoordinate
}
// 
func PlaceBlockInScreen(EmptyScreen [][]int,Block [][]int,Coordinate []int)[][]int{
	ScreenContainBlock:=CopyBlock(EmptyScreen)
	for row:=0;row<len(Block);row++{
		for colum:=0;colum<len(Block[row]);colum++{
			if Block[row][colum]!=0{
				if (row+Coordinate[0])<len(EmptyScreen){
					num:=Block[row][colum]
					ScreenContainBlock[row+Coordinate[0]][colum+Coordinate[1]]=num
				}
			}
		}
	}
	return ScreenContainBlock
}

func Down1RowByCoordinate(EmptyScreen [][]int,Block [][]int,Coordinate []int)[]int{
	NewCoordinate:=CopyCoordinate(Coordinate)
	NewBlock:=CopyBlock(Block)
	LastRow:=0
	for row:=range NewBlock{
		for colum:=range NewBlock[row]{
			if NewBlock[row][colum]!=0{
				LastRow=row	
			}
		}
	}
	if NewCoordinate[0]<len(EmptyScreen)-LastRow-1{
		NewCoordinate[0]+=1
		return NewCoordinate
	}else{
		return NewCoordinate
	}
}

// 
func main(){
	Screen:=InitScreen(20,10)
	BlockRand:=ListBlock[1]
	Coor:=[]int{0,3}
	Scr:=PlaceBlockInScreen(Screen,BlockRand,Coor)
	// fmt.Println(Scr)
	for row:=0;row<len(Scr);row++{
		fmt.Println(Scr[row])
	}
	ds:=TestBlockNext(Scr,Screen)
	fmt.Println(ds)
}