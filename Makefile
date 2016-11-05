JFLAGS = -g 
JC = javac

Class = Node.java Graph.java Main.java
Object = $(Class:.java=.class)

all: $(Object)

$(Object):$(Class)
	$(JC) $(JFLAGS) $^

clean:
	$(RM) *.class
