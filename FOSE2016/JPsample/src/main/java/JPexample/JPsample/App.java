package JPexample.JPsample;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.ConstructorDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.TypeDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;


/**
 * Hello world!
 *
 */
public class App 
{
	public static void main( String[] args ) throws Exception
    {
    	readFolder(new File("/Users/hideshi-s/Desktop/httpclient"));
    	System.out.println("Done!!");
    	/*
        FileInputStream in = new FileInputStream("/Users/hideshi-s/Documents/workspace/JPsample/src/main/java/JPexample/JPsample/Ctest1.java");
        CompilationUnit cu;
        try {
    	    cu = JavaParser.parse(in);
        } finally {
    	    in.close();
        }
        ClassGetter(cu);
        
        System.out.println("---------- On the Constructor ----------");
        ConstructorGetter(cu);
        System.out.println("---------- On the Method ----------");
        new MethodVisitor().visit(cu, null);
        */
    }
    
    public static void ClassGetter(CompilationUnit cu, String FileName) throws Exception {
        List<TypeDeclaration> typeDeclarations = cu.getTypes();
        if (typeDeclarations == null) {
        	return;
        }
        for (TypeDeclaration typeDec : typeDeclarations) {
        	//System.out.println("Class," + typeDec.getName() + "," + Integer.toString(typeDec.getBeginLine()) + "," + Integer.toString(typeDec.getEndLine()));
        	String ClassName = typeDec.getName();
        	List<BodyDeclaration> members = typeDec.getMembers();
        	if (members == null){
        		continue;
        	}
        	for (BodyDeclaration member : members){
    			if (member instanceof ConstructorDeclaration){
    				ConstructorDeclaration unko = (ConstructorDeclaration) member;
    				String[] OutputInfo = {FileName, ClassName, unko.getName(), Integer.toString(unko.getBeginLine()), Integer.toString(unko.getEndLine())}; 
    				File file = new File("hogehoge.csv");
    				PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(file, true)));
    				pw.println(String.join(",", OutputInfo));
    				pw.close();

        		} else if (member instanceof MethodDeclaration){
    				MethodDeclaration unko = (MethodDeclaration) member;
    				String[] OutputInfo = {FileName, ClassName, unko.getName(), Integer.toString(unko.getBeginLine()), Integer.toString(unko.getEndLine())};
    				File file = new File("hogehoge.csv");
    				PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(file, true)));
    				pw.println(String.join(",", OutputInfo));
    				pw.close();
    			}
        	}
        }
    }
    
    static void readFolder(File dir) throws Exception {
    	File[] files = dir.listFiles();
    	if (files ==null) {
    		return;
    	}
    	for (File file : files) {
    		if (!file.exists()) {
    			continue;
    		} else if (file.isDirectory()) {
    			readFolder(file);
    		} else if (file.isFile() && file.getPath().endsWith(".java")) {
    			//System.out.println(file.getPath());
    	        FileInputStream in = new FileInputStream(file.getPath());
    	        CompilationUnit cu;
    	        try {
    	    	    cu = JavaParser.parse(in);
    	        } finally {
    	    	    in.close();
    	        }
    	        ClassGetter(cu, file.getPath());
    		}
    	}
    	return;
    }

    /*
    public static void ConstructorGetter(CompilationUnit cu) {
        List<TypeDeclaration> typeDeclarations = cu.getTypes();
        for (TypeDeclaration typeDec : typeDeclarations) {
        	List<BodyDeclaration> members = typeDec.getMembers();
        	if (members != null){
        		for (BodyDeclaration member : members) {
        			if (member instanceof ConstructorDeclaration) {
        				ConstructorDeclaration constructor = (ConstructorDeclaration) member;
        				System.out.println(constructor.getName());
        				System.out.println(constructor.getBeginLine());
        				System.out.println(constructor.getEndLine());
        			}
        		}
        	}
        }
    }
    
    private static class MethodVisitor extends VoidVisitorAdapter {
    	@Override
    	public void visit(MethodDeclaration n, Object arg) {
    		System.out.println(n.getName());
    		System.out.println(n.getBeginLine());
    		System.out.println(n.getEndLine());
    		//System.out.println(n.getBody());
    		//System.out.println(n.getOrphanComments());
    		super.visit(n, arg);
    	}
    }
    */
}
