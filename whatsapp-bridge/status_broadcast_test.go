package main

import (
	"testing"

	"go.mau.fi/whatsmeow/types"
)

func TestIsStatusBroadcast(t *testing.T) {
	cases := []struct {
		name string
		jid  types.JID
		want bool
	}{
		{"status broadcast", types.StatusBroadcastJID, true},
		{"direct chat", types.NewJID("6588364624", types.DefaultUserServer), false},
		{"group chat", types.NewJID("120363403881494595", types.GroupServer), false},
	}
	for _, tc := range cases {
		if got := isStatusBroadcast(tc.jid); got != tc.want {
			t.Errorf("%s: isStatusBroadcast(%s) = %v, want %v", tc.name, tc.jid, got, tc.want)
		}
	}
}
