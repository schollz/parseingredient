package main

import (
	"bufio"
	"bytes"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/boltdb/bolt"
	"gopkg.in/cheggaaa/pb.v1"
)

func lineCounter(r io.Reader) (int, error) {
	buf := make([]byte, 32*1024)
	count := 0
	lineSep := []byte{'\n'}

	for {
		c, err := r.Read(buf)
		count += bytes.Count(buf[:c], lineSep)

		switch {
		case err == io.EOF:
			return count, nil

		case err != nil:
			return count, err
		}
	}
}

func hash(str string) string {
	hasher := md5.New()
	hasher.Write([]byte(str))
	return hex.EncodeToString(hasher.Sum(nil))
}

func generateBuckets(filename string) {
	type Message struct {
		Text        string
		Ingredients []string
	}

	// Open the my.db data file in your current directory.
	// It will be created if it doesn't exist.
	db, err := bolt.Open("my.db", 0600, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Create bucket if it doesn't exist
	db.Update(func(tx *bolt.Tx) error {
		_, err2 := tx.CreateBucketIfNotExists([]byte(filename))
		if err2 != nil {
			return fmt.Errorf("create bucket: %s", err2)
		}
		_, err2 = tx.CreateBucketIfNotExists([]byte(filename + "String"))
		if err2 != nil {
			return fmt.Errorf("create bucket: %s", err2)
		}
		return nil
	})

	// Count the number of lines in file
	file, err := os.Open("test2")
	if err != nil {
		log.Fatal(err)
	}
	lines, _ := lineCounter(file)
	file.Close()

	// Open the file for streaming JSON
	file, err = os.Open("test2")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Read in file line by line
	scanner := bufio.NewScanner(file)
	bar := pb.StartNew(lines)
	db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(filename))
		b2 := tx.Bucket([]byte(filename + "String"))
		for scanner.Scan() {
			dec := json.NewDecoder(strings.NewReader(scanner.Text()))
			bar.Increment()
			for {
				// Read in the JSON line
				var m Message
				if err := dec.Decode(&m); err == io.EOF {
					break
				} else if err != nil {
					log.Fatal(err)
				}

				// Hash the text and check if it exists before continuing
				hashText := hash(m.Text)
				v := b2.Get([]byte(hashText))
				if v != nil {
					continue
				}
				b2.Put([]byte(hashText), []byte(m.Text))

				text := []string{hashText}
				for _, ingredient := range m.Ingredients {
					v := b.Get([]byte(ingredient))
					if v == nil {
						bText, _ := json.Marshal(text)
						b.Put([]byte(ingredient), bText)
					} else {
						var currentTexts []string
						errExtractText := json.Unmarshal(v, &currentTexts)
						if errExtractText != nil {
							fmt.Println("error:", errExtractText)
						}
						text = append(text, currentTexts...)
						bText, _ := json.Marshal(text)
						b.Put([]byte(ingredient), bText)
					}
				}

			}
		}

		return nil
	})
	bar.FinishPrint("Finished loading.")
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}

	db.View(func(tx *bolt.Tx) error {
		// Assume bucket exists and has keys
		b := tx.Bucket([]byte(filename))

		c := b.Cursor()

		for k, v := c.First(); k != nil; k, v = c.Next() {
			var currentTexts []string
			errExtractText := json.Unmarshal(v, &currentTexts)
			if errExtractText != nil {
				fmt.Println("error:", errExtractText)
			}
			fmt.Printf("key=%s, value=%v\n", k, len(currentTexts))
		}

		return nil
	})

	// db.View(func(tx *bolt.Tx) error {
	// 	// Assume bucket exists and has keys
	// 	b := tx.Bucket([]byte("ingredientString"))
	//
	// 	c := b.Cursor()
	//
	// 	for k, v := c.First(); k != nil; k, v = c.Next() {
	// 		fmt.Printf("key=%s, value=%s\n", k, v)
	// 	}
	//
	// 	return nil
	// })

}

func main() {
	generateBuckets("test")
}
