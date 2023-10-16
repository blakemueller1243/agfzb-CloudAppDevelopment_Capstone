# Use the official Node.js image as our base image
FROM node:16

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Expose the ports the app runs on
EXPOSE 3000 3001

# Define the command to run the app
CMD ["npm", "start"]
