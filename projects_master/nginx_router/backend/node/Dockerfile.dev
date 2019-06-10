# Pull base image
FROM node:6.17-alpine

# Set working container path for commands
WORKDIR /usr/my_node_app

# Copy files over
COPY ./package.json ./

# SET UP DEPENDENCIES
RUN npm install

COPY ./ ./

# Default command
CMD ["npm", "start"]
