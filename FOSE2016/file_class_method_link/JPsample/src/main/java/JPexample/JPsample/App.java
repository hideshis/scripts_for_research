package JPexample.JPsample;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.TypeParameter;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.ConstructorDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
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
    	readFolder(new File(args[0]), args[1]);
    	System.out.println("Done!!");
    }
	
	static void readFolder(File dir, String outputFilePath) throws Exception {
    	File[] files = dir.listFiles();
    	if (files ==null) {
    		return;
    	}
    	for (File file : files) {
    		if (!file.exists()) {
    			continue;
    		} else if (file.isDirectory()) {
    			readFolder(file, outputFilePath);
    		} else if (file.isFile() && file.getPath().endsWith(".java")) {
    			//System.out.println(file.getPath());
    	        FileInputStream in = new FileInputStream(file.getPath());
    	        CompilationUnit cu;
    	        try {
    	    	    cu = JavaParser.parse(in);
    	        } finally {
    	    	    in.close();
    	        }
    	        ClassGetter(cu, file.getPath(), outputFilePath);
    		}
    	}
    	return;
    }	
	
    public static void ClassGetter(CompilationUnit cu, String FileName, String outputFilePath) throws Exception {
        List<TypeDeclaration> typeDeclarations = cu.getTypes();
        if (typeDeclarations == null) {
        	return;
        }
        for (TypeDeclaration typeDec : typeDeclarations) {
        	String ClassName = typeDec.getName();
    		String[] OutputInfo = {FileName, ClassName, Integer.toString(typeDec.getBeginLine()), Integer.toString(typeDec.getEndLine())};
    		File file = new File(outputFilePath + "/file_class.csv");
    		PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(file, true)));
    		pw.println(String.join("|", OutputInfo));
    		pw.close();

        	List<BodyDeclaration> members = typeDec.getMembers();
        	if (members == null){
        		continue;
        	}
        	for (BodyDeclaration member : members){
    			if (member instanceof ConstructorDeclaration){
    				ConstructorDeclaration unko = (ConstructorDeclaration) member;
    				System.out.println(FileName + "," + unko.getName());
    				System.out.println(unko.getParameters().toString());
    				fileOutput(outputFilePath, FileName, ClassName, unko.getName(), 
    						unko.getParameters(), Integer.toString(unko.getBeginLine()), Integer.toString(unko.getEndLine()));
        		} else if (member instanceof MethodDeclaration){
    				MethodDeclaration unko = (MethodDeclaration) member;
    				System.out.println(FileName + "," + unko.getName());
    				System.out.println(unko.getParameters().toString());
    				fileOutput(outputFilePath, FileName, ClassName, unko.getName(), 
    						unko.getParameters(), Integer.toString(unko.getBeginLine()), Integer.toString(unko.getEndLine()));
    			}
        	}
        }
    }
    
    private static void fileOutput(String outputFilePath, String FileName, String ClassName, String MethodName, List<Parameter> parameters,
			String BeginLine, String EndLine) throws Exception {
		ArrayList paramList = getParameters(parameters);
		String[] OutputInfo = {FileName, ClassName, MethodName, String.join(",", paramList), BeginLine, EndLine};
		File file = new File(outputFilePath + "/file_class_method.csv");
		PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(file, true)));
		pw.println(String.join("|", OutputInfo));
		pw.close();
	}
    
	public static ArrayList getParameters(List<Parameter> ParameterList) {
		ArrayList paramList = new ArrayList();
		for (Parameter param: ParameterList) {
			String paramString = param.toString();
			if (paramString.startsWith("final ")) {
				paramString = paramString.replace("final ", "");
			}
			paramString = paramString.split(" ")[0];
			if (paramString.contains("<")) {
				paramString = paramString.replaceFirst("<.*", "");
			}
			if (paramString.endsWith("...")) {
				System.out.println("oppai");
				paramString= paramString.replace("...", "[]");
			}
			paramList.add(paramString);
		}
		System.out.println(paramList.toString());
		return paramList;		
	}
  }
