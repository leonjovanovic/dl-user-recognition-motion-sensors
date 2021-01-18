import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

public class createTests {

	public static void main(String[] args) {
		PrintWriter writer = null;
		try {
			writer = new PrintWriter("tests.txt", "UTF-8");
		} catch (FileNotFoundException | UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		int cnt = 0;
		String data = "";
		for(int o = 0; o<3; o++) //jezik
			for(int l = 0; l<3; l++) //distanca
				for(int i = 0; i<3; i++) //izvor zvuka
					for(int j = 0; j<3; j++) //broj osoba
						for(int k = 0; k<5; k++) //lokacija
							for(int m = 0; m<3; m++) //pol
								for(int n = 0; n<3; n++) //godine
								{ 
									if(notPossibleTest(i,j,k,l,m,n,o)) continue;
									System.out.println(cnt++);
									data = "";
									data += writeSource(writer,i,j,k,l,m,n,o);
									data += writeNumPers(writer,i,j,k,l,m,n,o);
									data += writeLocation(writer,i,j,k,l,m,n,o);
									data += writeDistance(writer,i,j,k,l,m,n,o);
									data += writeGender(writer,i,j,k,l,m,n,o);
									data += writeYears(writer,i,j,k,l,m,n,o);
									data += writeLanguage(writer,i,j,k,l,m,n,o);
									writer.println(data);
								}
		writer.close();

	}
	
	private static String writeLanguage(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<3; ii++) {
			if(ii == o)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;	
	}

	private static String writeYears(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<3; ii++) {
			if(ii == n)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;		
	}

	private static String writeGender(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		if(m == 2) return "YES\tYES\t";
		else if (m == 1) return "NO\tYES\t";
		else return "YES\tNO\t";
	}

	private static String writeDistance(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<3; ii++) {
			if(ii == l)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;	
	}

	private static String writeLocation(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<5; ii++) {
			if(ii == k)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;			
	}

	private static String writeNumPers(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<3; ii++) {
			if(ii == j)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;		
	}

	private static String writeSource(PrintWriter writer, int i, int j, int k, int l, int m, int n, int o) {
		String temp = "";
		for(int ii = 0; ii<3; ii++) {
			if(ii == i)temp+="YES\t";
			else temp+="NO\t";
		}
		return temp;		
	}

	public static boolean notPossibleTest(int i, int j, int k, int l, int m, int n, int o) {
		if(i == 0) {
			if(k>1)return true;
			if(l>1)return true;
			if(j>1 && o>1) return true;
		}
		if(i == 1) {
			if(j>0)return true;
		}
		if(i == 2) {
			if(n<1) return true;
			if(o == 2 && n!= 1) return true;
			if(o == 1 && n!= 1) return true;
		}
		if(k == 0 || k == 1) {
			if(l>1)return true;
		}		
		if(m == 2) {
			if(j == 0) return true;
		}
		
		return false;
	}

}
