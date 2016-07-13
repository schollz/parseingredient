package main

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/boltdb/bolt"
	"github.com/deckarep/golang-set"
	"gopkg.in/cheggaaa/pb.v1"
)

var db *bolt.DB

// itob returns an 8-byte big endian representation of v.
func itob(v uint64) []byte {
	b := make([]byte, 8)
	binary.BigEndian.PutUint64(b, uint64(v))
	return b
}

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

func linesInFile(fileName string) (int, error) {
	// Count the number of lines in file
	file, err := os.Open(fileName)
	if err != nil {
		return -1, err
	}
	lines, _ := lineCounter(file)
	file.Close()
	return lines, nil
}

// JSONLine is the data in each line of the file
type JSONLine struct {
	Text        string
	Ingredients []string
}

func generateDatabase(databaseName string) {

	// Open the my.db data file in your current directory.
	// It will be created if it doesn't exist.
	var err error
	db, err = bolt.Open(databaseName+".db", 0600, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Get the number of the lines for the progress bar
	var numberOfLines int
	numberOfLines, err = linesInFile(databaseName + ".txt")
	if err != nil {
		log.Fatal(err)
	}

	// Open the file for streaming JSON
	fmt.Println("Collecting all ingredients...")
	allIngredients := mapset.NewSet()
	file, err := os.Open(databaseName + ".txt")
	if err != nil {
		log.Fatal(err)
	}
	bar := pb.StartNew(numberOfLines)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		dec := json.NewDecoder(strings.NewReader(scanner.Text()))
		bar.Increment()
		for {
			var m JSONLine
			if err = dec.Decode(&m); err == io.EOF {
				break
			} else if err != nil {
				log.Fatal(err)
			}
			for _, ingredient := range m.Ingredients {
				allIngredients.Add(ingredient)
			}
		}
	}
	file.Close()
	bar.FinishPrint("Finished loading.")
	if err = scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	fmt.Println("Creating buckets for each ingredient...")
	err = db.Update(func(tx *bolt.Tx) error {
		_, err1 := tx.CreateBucket([]byte("noingredients"))
		if err1 != nil {
			return fmt.Errorf("create bucket: %s", err1)
		}
		_, err1 = tx.CreateBucket([]byte("texts"))
		if err1 != nil {
			return fmt.Errorf("create bucket: %s", err1)
		}
		for _, ingredient := range allIngredients.ToSlice() {
			_, err2 := tx.CreateBucket([]byte(ingredient.(string)))
			if err2 != nil {
				return fmt.Errorf("create bucket: %s", err2)
			}
		}
		return nil
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Inserting data into buckets...")
	file, err = os.Open(databaseName + ".txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner = bufio.NewScanner(file)
	bar = pb.StartNew(numberOfLines)
	err = db.Update(func(tx *bolt.Tx) error {
		for scanner.Scan() {
			dec := json.NewDecoder(strings.NewReader(scanner.Text()))
			bar.Increment()
			for {
				var m JSONLine
				if err = dec.Decode(&m); err == io.EOF {
					break
				} else if err != nil {
					log.Fatal(err)
				}

				b := tx.Bucket([]byte("texts"))
				if b == nil {
					return fmt.Errorf("doesn't exist")
				}
				id, _ := b.NextSequence()
				m.Text = strings.Split(strings.Split(m.Text, " - recipe -")[0], " | epicurious")[0]
				b.Put(itob(id), []byte(m.Text))

				for _, ingredient := range m.Ingredients {
					b2 := tx.Bucket([]byte(ingredient))
					if b2 == nil {
						return fmt.Errorf("doesn't exist")
					}
					id2, _ := b2.NextSequence()
					b2.Put(itob(id2), itob(id))
				}

			}
		}
		return nil
	})
	if err != nil {
		log.Fatal(err)
	}
	file.Close()
	bar.FinishPrint("Finished loading.")
	if err = scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}

}

func check(databaseName string) {
	var err error
	db, err = bolt.Open(databaseName+".db", 0600, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("apples"))
		c := b.Cursor()
		for k, v := c.First(); k != nil; k, v = c.Next() {
			b2 := tx.Bucket([]byte("texts"))
			fmt.Printf("key=%v, value=%v, found=%v\n", k, v, string(b2.Get(v)))
		}
		return nil
	})
}

func main() {
	generateDatabase("markov_title.0")
	check("titles")
}
