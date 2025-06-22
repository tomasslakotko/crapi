# Crew Roster Parser Application 📋✈️

A web application for parsing airline crew roster PDF files into structured CSV data. Built for parsing NetLine/Crew roster documents.

## Features ✨

- **PDF Upload Interface**: Clean web interface for uploading roster PDFs
- **Smart 3-Column Parser**: Correctly handles complex PDF layouts with 3 columns
- **Date-Flight Association**: Accurately links flights to their corresponding dates  
- **CSV Export**: Converts parsed data to structured CSV format
- **REST API**: Programmatic access with API key authentication
- **Real-time Processing**: Live feedback during file processing

## Recent Improvements 🚀

- ✅ **Fixed Mon02 DAYOFF Issue**: Resolved incorrect flight assignment to dates
- ✅ **3-Column Layout Support**: Proper handling of complex roster structures  
- ✅ **Coordinate-Based Parsing**: Uses PDF text positioning for accurate extraction
- ✅ **Flight-Date Accuracy**: Each flight correctly associated with its date

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pards
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 💻

### Web Interface

1. **Start the server**:
   ```bash
   node server.js
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:3000
   ```

3. **Upload a PDF** roster file and get structured CSV output

### API Usage

**Endpoint**: `POST /api/parse`

**Headers**:
```
Content-Type: multipart/form-data
X-API-Key: your-api-key
```

**Body**: Form data with `pdfFile` field containing the PDF

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "Date": "Sun01",
      "Weekday": "Sun", 
      "Day Number": "01",
      "Duty Type": "DAYOFF",
      "Duty Location": "VIE"
    }
  ]
}
```

## File Structure 📁

```
pards/
├── server.js                 # Main Node.js server
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies  
├── public/
│   └── index.html            # Web interface
├── netline-crewlink-parser/
│   ├── parser.py             # PDF parser (improved)
│   └── TXTtoCSV.py          # CSV converter
├── uploads/                  # Uploaded PDF files
└── outputs/                  # Generated CSV files
```

## Supported Data 📊

The parser extracts and structures:

- **Dates**: Sun01, Mon02, etc.
- **Duty Types**: DAYOFF, C/I (Check-In), FLIGHT
- **Flight Information**: Numbers, routes, times, aircraft types
- **Locations**: Airport codes (VIE, BER, ARN, etc.)
- **Times**: Departure/arrival times in 24h format

## Example Output 📋

| Date | Weekday | Duty Type | Flight Number | Departure | Arrival | Aircraft |
|------|---------|-----------|---------------|-----------|---------|----------|
| Sun01| Sun     | DAYOFF    | -             | -         | VIE     | -        |
| Mon02| Mon     | DAYOFF    | -             | -         | VIE     | -        |
| Sat14| Sat     | FLIGHT    | OS 311        | VIE       | ARN     | A220     |

## Development 🔧

### Parser Testing

Test the parser directly:
```bash
python3 netline-crewlink-parser/parser.py uploads/roster.pdf outputs
python3 netline-crewlink-parser/TXTtoCSV.py outputs/combined_cleaned_roster.txt outputs
```

### Environment Variables

- `API_KEY`: Set for production API authentication
- `PORT`: Server port (default: 3000)

## Docker Support 🐳

Build and run with Docker:
```bash
docker build -t crew-roster-parser .
docker run -p 3000:3000 crew-roster-parser
```

## Known Issues & Fixes 🔧

- **✅ SOLVED**: Mon02 incorrectly showing flights instead of DAYOFF
- **✅ SOLVED**: Flight-date misassociation across columns
- **✅ SOLVED**: 3-column PDF layout parsing issues

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License.

## Author ✍️

Created for parsing NetLine/Crew roster documents with accuracy and efficiency.

---

**Status**: ✅ **Production Ready** - Parser successfully handles complex 3-column layouts with accurate date-flight associations. 