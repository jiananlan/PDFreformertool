go
package main

import "fmt"

type Attachment struct {
	DownloadURL string `json:"downloadUrl"`
}

type Data struct {
	OID         string       `json:"oid"`
	EnvelopeTo  string       `json:"envelope_to"`
	Attachments []Attachment `json:"attachments"`
}

func main() {
	a := Data{
		OID:        "50407-6rb9k-oc6iu7bbLEQG2eDvmZGEci",
		EnvelopeTo: "6rb9k.test@inbox.testmail.app",
		Attachments: []Attachment{
			{
				DownloadURL: "https://object.testmail.app/api/50407-6rb9k-oc6iu7bbLEQG2eDvmZGEci/cY29iMuXthe7yZYbtMLs1F/1I6A2277.CR3",
			},
		},
	}

	fmt.Println(a.OID)
	fmt.Println(a.EnvelopeTo)
	fmt.Println(a.Attachments[0].DownloadURL)
}
