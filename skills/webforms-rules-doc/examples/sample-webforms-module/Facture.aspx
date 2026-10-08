<%@ Page Language="VB" AutoEventWireup="false" CodeBehind="Facture.aspx.vb" Inherits="Legacy.Facture" %>
<asp:TextBox ID="txtMontant" runat="server" />
<asp:RequiredFieldValidator ID="rfvMontant" runat="server" ControlToValidate="txtMontant" ErrorMessage="Le montant est obligatoire" />
<asp:Button ID="btnValider" runat="server" Text="Valider" />
