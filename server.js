const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { execFile } = require('child_process');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    console.log('📁 Saving file to uploads directory...');
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    const filename = 'roster_' + Date.now() + '.pdf';
    console.log('📄 File will be saved as:', filename);
    cb(null, filename);
  }
});

const upload = multer({ 
  storage: storage,
  fileFilter: function (req, file, cb) {
    console.log('🔍 Checking file type:', file.mimetype);
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      console.log('❌ Invalid file type:', file.mimetype);
      cb(new Error('Only PDF files are allowed!'), false);
    }
  }
});

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
  console.log('📁 Creating uploads directory...');
  fs.mkdirSync('uploads');
}
if (!fs.existsSync('outputs')) {
  console.log('📁 Creating outputs directory...');
  fs.mkdirSync('outputs');
}

// Helper function to convert CSV to JSON array
const csvToJson = (csvString) => {
    const lines = csvString.trim().split('\n');
    if (lines.length < 2) return []; // Return empty if only header or empty
    
    const headers = lines[0].split(',').map(h => h.trim());
    const result = [];
    
    for (let i = 1; i < lines.length; i++) {
        const obj = {};
        const currentline = lines[i].split(',');
        
        headers.forEach((header, j) => {
            obj[header] = currentline[j] ? currentline[j].trim() : '';
        });
        result.push(obj);
    }
    return result;
};

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Helper function to run python scripts
const runPythonScript = (script, args) => {
  return new Promise((resolve, reject) => {
    // Corrected path for Docker container environment
    const scriptPath = path.join('/app', script);
    console.log(`🐍 Running Python script: python3 ${scriptPath} ${args.join(' ')}`);

    execFile('python3', [scriptPath, ...args], (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Error executing ${script}:`, error);
        console.error(`stderr: ${stderr}`);
        return reject(error);
      }
      console.log(`✅ ${script} stdout:`, stdout);
      if (stderr) {
        console.warn(`⚠️ ${script} stderr:`, stderr);
      }
      resolve(stdout);
    });
  });
};

app.post('/upload', upload.single('pdfFile'), async (req, res) => {
  try {
    console.log('🚀 Starting file upload processing...');
    
    if (!req.file) {
      console.log('❌ No file uploaded');
      return res.status(400).json({ error: 'No file uploaded' });
    }

    console.log('✅ File uploaded successfully:', req.file.filename);
    const pdfPath = req.file.path;
    const outputDir = path.join(__dirname, 'outputs');
    const combinedTxtPath = path.join(outputDir, 'combined_cleaned_roster.txt');
    const csvPath = path.join(outputDir, 'parsed_schedule.csv');

    // 1. Run the PDF parser
    await runPythonScript('parser.py', [pdfPath, outputDir]);
    
    // 2. Run the CSV converter
    await runPythonScript('TXTtoCSV.py', [combinedTxtPath, outputDir]);

    console.log('📖 Reading CSV file:', csvPath);
    if (fs.existsSync(csvPath)) {
      const csvData = fs.readFileSync(csvPath, 'utf8');
      console.log('✅ CSV file read successfully, size:', csvData.length, 'characters');
      res.json({ 
        success: true, 
        message: 'File processed successfully',
        csvData: csvData,
        downloadUrl: `/download/${path.basename(csvPath)}`
      });
    } else {
      console.log('❌ CSV file not found at:', csvPath);
      res.status(500).json({ error: 'CSV file not generated' });
    }

  } catch (error) {
    console.error('❌ Error processing file:', error);
    res.status(500).json({ error: 'Error processing file: ' + error.message });
  }
});

// New API endpoint for programmatic access
app.post('/api/parse', upload.single('pdfFile'), async (req, res) => {
  const tempFiles = [];
  try {
    console.log('🤖 API: Starting file upload processing...');
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }
    tempFiles.push(req.file.path); // Mark for cleanup

    const pdfPath = req.file.path;
    const outputDir = path.join(__dirname, 'outputs');
    const combinedTxtPath = path.join(outputDir, `api_temp_${Date.now()}.txt`);
    const csvPath = path.join(outputDir, `api_temp_${Date.now()}.csv`);
    tempFiles.push(combinedTxtPath, csvPath); // Mark for cleanup

    // 1. Run the PDF parser
    await runPythonScript('parser.py', [pdfPath, outputDir]);
    
    // 2. Run the CSV converter
    await runPythonScript('TXTtoCSV.py', [path.join(outputDir, 'combined_cleaned_roster.txt'), outputDir]);

    if (fs.existsSync(path.join(outputDir, 'parsed_schedule.csv'))) {
      const csvData = fs.readFileSync(path.join(outputDir, 'parsed_schedule.csv'), 'utf8');
      const jsonData = csvToJson(csvData);
      console.log('🤖 API: Successfully parsed data. Sending JSON response.');
      res.json({ success: true, data: jsonData });
    } else {
      res.status(500).json({ success: false, error: 'API: Parsed CSV file not found' });
    }
  } catch (error) {
    console.error('❌ API Error processing file:', error);
    res.status(500).json({ success: false, error: 'API: Error processing file: ' + error.message });
  } finally {
    // Cleanup temporary files
    tempFiles.forEach(filePath => {
      fs.unlink(filePath, err => {
        if (err) console.error(`🧹 Error cleaning up temp file ${filePath}:`, err);
      });
    });
  }
});

app.get('/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, 'outputs', filename);
  
  if (fs.existsSync(filePath)) {
    res.download(filePath);
  } else {
    res.status(404).json({ error: 'File not found' });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
  console.log(`🌐 Open http://localhost:${PORT} in your browser`);
}); 