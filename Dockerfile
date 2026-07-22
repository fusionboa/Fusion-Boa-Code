# FusionBoa Language — Try it without installing anything!
#
# Build:   docker build -t fusionboa .
# Run:     docker run --rm fusionboa fusionboa --help
# Build:   docker run --rm -v $(pwd):/app fusionboa fusionboa build myfile.fusboa
#
# For the complete 23-target demo:
#   docker run --rm fusionboa fusionboa build complete_test.fusboa
#   # Output goes to /root/Desktop/ inside container
#   docker run --rm fusionboa ls -la /root/Desktop/fusionboa-*/

FROM python:3.12-slim

WORKDIR /app

# Copy the entire project
COPY . .

# Install FusionBoa
RUN pip install -e . --quiet --no-cache-dir

# Test that it works
RUN python fusionboa.py version

# Default: show help
CMD ["fusionboa", "--help"]
