// Power Query (M) - paste into Home > Transform data > Advanced Editor
// Update the file path to where data/sales_data.csv lives on your machine.
let
    Source        = Csv.Document(File.Contents("C:\path\to\data\sales_data.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted      = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed         = Table.TransformColumnTypes(Promoted, {
                        {"OrderID", type text}, {"OrderDate", type date}, {"ShipMode", type text},
                        {"Segment", type text}, {"Region", type text}, {"Category", type text},
                        {"SubCategory", type text}, {"Quantity", Int64.Type}, {"Discount", type number},
                        {"Sales", type number}, {"Profit", type number}}),
    NoDuplicates  = Table.Distinct(Typed, {"OrderID"}),
    NoNulls       = Table.SelectRows(NoDuplicates, each [Sales] <> null and [OrderDate] <> null),
    AddYear       = Table.AddColumn(NoNulls, "Year", each Date.Year([OrderDate]), Int64.Type),
    AddMonthNum   = Table.AddColumn(AddYear, "MonthNumber", each Date.Month([OrderDate]), Int64.Type),
    AddMonthName  = Table.AddColumn(AddMonthNum, "MonthName", each Date.ToText([OrderDate], "MMM"), type text)
in
    AddMonthName
