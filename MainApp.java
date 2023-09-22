/**
 * MainApp
 * Autore: Pintescul Patric
 */
public class MainApp {

    
    public static void main(String[] args) {
        int[][] matrice = creaMatrice(2);
        System.out.println("SOMMA DIAGONALE PRINCIPALE -> "+sommaDiagonalePrincipale(matrice));
        
        System.out.println("MATRICE:");
        // stampa la matrice
        for (int i = 0; i < matrice.length; i++) {
            if(i==0)System.out.println("*----".repeat(matrice.length)+"*");
            for (int j = 0; j < matrice.length; j++) {
                if (j==0)System.out.print("|");
                System.out.printf(" %2d |", matrice[i][j]);
            }
            System.out.println();
            System.out.println("*----".repeat(matrice.length)+"*");
        }
    }

    // metodo per creare una matrice di n*n e popolarla di numeri random da 1 a 50
    public static int[][] creaMatrice(int n) {
        int[][] matrice = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                matrice[i][j] = (int) (Math.random() * 50) + 1;
            }
        }
        return matrice;
    }

    // sviluppare un metodo
    // che data una matrice
    // n*n di numeri interi
    // restituisca la somma degli elementi della diagonale principale

    /**
     * Calcola la somma degli elementi sulla diagonale principale della matrice.
     * 
     * @param matrice La matrice n*n di numeri interi.
     * @return La somma degli elementi sulla diagonale principale.
     */
    public static int sommaDiagonalePrincipale(int[][] matrice) {
        int somma = 0;
        for (int i = 0; i < matrice.length; i++) {
            somma += matrice[i][i];
        }
        return somma;
    }
}
