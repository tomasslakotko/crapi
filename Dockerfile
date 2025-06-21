FROM node:16-alpine

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy application code
# Explicitly copy the parser directory first
COPY netline-crewlink-parser /app/netline-crewlink-parser
# Then copy the rest of the app's files
COPY package.json package-lock.json server.js ./
COPY public ./public

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 