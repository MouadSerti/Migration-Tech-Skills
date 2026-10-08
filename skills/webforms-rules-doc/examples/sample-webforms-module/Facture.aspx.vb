Public Class Facture
    Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
        If Not IsPostBack Then
            btnValider.Enabled = Session("Role") = "Manager"
        End If
    End Sub

    Protected Sub btnValider_Click(sender As Object, e As EventArgs) Handles btnValider.Click
        If Page.IsValid Then
            Dim montant As Decimal = CDec(txtMontant.Text)
            If montant > 10000 Then
                Throw New Exception("Plafond depasse")
            End If
            SaveFacture(montant)
        End If
    End Sub
End Class
