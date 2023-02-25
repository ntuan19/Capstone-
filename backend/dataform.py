from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, DecimalField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length


class InvestmentForm(FlaskForm):
    business_registration = StringField('Business Registration', validators=[DataRequired(), Length(max=50)])
    business_address = StringField('Business Address', validators=[DataRequired(), Length(max=100)])
    company_name = StringField("Company's Name", validators=[DataRequired(), Length(max=50)])
    current_rounds = IntegerField('Current Rounds of Investments', validators=[DataRequired()])
    total_funding_wanted = DecimalField('Total Funding Wanted', validators=[DataRequired()])
    currency = SelectField("Currency", choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('JPY', 'JPY')])
    presentation = FileField('Presentation')
    pictures = FileField('Pictures')
    financial_situation = TextAreaField('Financial Situation', validators=[DataRequired()])
    approved = HiddenField('Approved', default='pending')
    tax_returns = FileField("Tax Returns",validators=[DataRequired()])
    financial_statements = FileField("Financial Statements",validators=[DataRequired()])
    customers_dataset = FileField("Customer Base",validators=[DataRequired()])
    supporting_documents = FileField("Supporting Documents")


