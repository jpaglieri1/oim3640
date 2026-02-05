for i in range(1, 4):
    print("Iteration:", i)
    print("Square",i*i)
    print()

def double(number):
    """Return double the input number"""
    return number*2

print(double(5))
print(double("5"))

def f():
    message = "hello"
    x = 5
    return message

print(f())
#print(x)
#print(message)

#Draw a square
def draw_square(size):
    """Create a square using python functions"""
    for i in range(size):
        print("🧱"*size)

draw_square(4)

#Draw a triangle
def draw_triangle(size):
    """Create a fucntion to draw a triangle"""
    for i in range(size):
        print("🧱"*(i+1))

draw_triangle(4)

#Draw a triangle like this
    #
   ##
  ###
 ####
#####

def draw_triangle2(size):
    """Create a triangle like the picture above"""
    for i in range(size):
        print(" "*(size-i)+"#"*(i+1))

draw_triangle2(5)

def draw_pyramid(size):
    """Create a pyramid using #s"""
    for i in range(size):
        print(" "*(size-i)+"#"+"#"*(i*2)+" "*(size-i))

draw_pyramid(5)