import heapq
import os

class H_Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_h_tree(data):
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1

    heap = [H_Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = H_Node(None, left.freq + right.freq)
        merged.left, merged.right = left, right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, current_code="", codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0", codes)
        generate_codes(node.right, current_code + "1", codes)
    return codes

def compress(text, output_file):
    root = build_h_tree(text)
    codes = generate_codes(root)

    compressed_data = "".join(codes[char] for char in text)
    padding = 8 - len(compressed_data) % 8
    compressed_data += "0" * padding

    with open(output_file, "w") as f:
        f.write(compressed_data)

    return codes

if __name__ == "__main__":
    input_file = input("Enter the path to the input file: ")

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        output_directory = input("Enter the path to the output directory: ")

        os.makedirs(output_directory, exist_ok=True)

        compressed_file = os.path.join(output_directory, "compressed.txt")

        try:
            with open(input_file, "r") as f:
                data = f.read()

            if not data:
                print("Input file is empty.")

            else:
                codes = compress(data, compressed_file)

                print("Huffman Codes:")
                for char, code in codes.items():
                    print(f"{char}: {code}")

                print(f"Compression successful. Output saved to {compressed_file}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

