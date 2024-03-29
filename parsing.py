#!/usr/bin/env python3

"""
Game of Thrones chapters vs episodes chart generator
Copyright (c) 2013-2018, Joel Geddert

This script generates an HTML file of the table.

Software License:
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

A note from the author:
	The original chart generated by this code, as well as all remaining applicable
	source & asset files (except where noted), are licensed under a Creative Commons
	BY-SA 4.0 license <http://creativecommons.org/licenses/by-sa/4.0/>. If you are
	going to use any of this code to create a derivative work, please respect this
	CC license.
"""


from utils import *
from book_show_types import *
import os.path
import csv


def parse_books(filename):
	book_list = []

	with open(filename) as csv_file:
		reader = csv.reader(csv_file)
		headers = next(reader)

		n = 1
		for row in reader:

			# Skip blank rows
			if not any(row):
				continue

			book_dict = {header: value for header, value in zip(headers, row)}
			book_list.append(Book(number=n, **book_dict))
			n += 1

	return book_list


def parse_chapters(filename, book_list):
	chapter_list = []
	total_chap_num = 0

	with open(filename) as csvFile:
		reader = csv.reader(csvFile)
		next(reader)

		for row in reader:
			if not any(row):
				continue

			# A few fields in here are from functionality that never got implemented
			# e.g. color by storyline or location
			book_name, chap_num_in_book, chap_name, pov_char, _, _, _, occurred = row

			book = find_unique(book_list, lambda book: book.name == book_name)
			chap_num_in_book = int(chap_num_in_book) + 1  # 0-indexed in csv (i.e. prologue is 0)

			if chap_num_in_book != len(book.chapters) + 1:
				raise ValueError('Chapter number in book does not match order: expected number %i, row %s' % (
					len(book.chapters) + 1, str(row)))

			if not pov_char:
				# if no POV char given in CSV file, use first word of chapter name
				pov_char = row[2].split()[0]
				if pov_char[0:3].lower() in ["pro", "epi"]:
					# If it's a prologue/epilogue then always make it "other"
					pov_char = "Other"
				elif pov_char[0:3].lower() == "the":
					# If it's a "the" chapter, there should be a pov char set!
					warn("no POV char given for chapter " + chap_name)
					pov_char = "Other"

			occurred = bool(int(occurred))

			total_chap_num += 1

			chapter = Chapter(
				number=total_chap_num,
				book=book,
				number_in_book=chap_num_in_book,
				name=chap_name,
				pov=pov_char,
				occurred=occurred,
			)

			chapter_list.append(chapter)
			book.chapters.append(chapter)

	debug_print(repr(chapter_list[0:10]))

	return chapter_list


def parse_combined_order(filename, chapters, books):

	combined_book = Book(
		45,
		'A Feast for Crows & A Dance with Dragons (Chronological)',
		abbreviation='AFfC + ADwD',
		combined_books=[books[3], books[4]])

	with open(filename, 'rU') as txt_file:
		while True:
			line = txt_file.readline()
			if not line:
				break

			words = line.split()
			words = [word.lower() for word in words]

			if 'affc' in words:
				book_num = 4
				n = words.index('affc')
			elif 'adwd' in words:
				book_num = 5
				n = words.index('adwd')
			else:
				print("ERROR: neither AFFC nor ADWD not found in line:")
				print(line)
				continue

			# combined.txt 1-indexes chapters
			chap_num = int(words[n + 1]) - 1

			chapter = chapters[chap_num + books[book_num - 1].chapters[0].number - 1]
			combined_book.chapters.append(chapter)

			debug_print(chapter)
			debug_print(line)

	return combined_book


def parse_episodes(filename):
	episode_list = []
	season_list = []

	with open(filename) as csvFile:

		reader = csv.reader(csvFile)
		next(reader)
		number = 0

		for row in reader:
			if not any(row):
				continue

			season_num, number_from_csv, num_in_season, name = row

			number += 1

			num_in_season = int(num_in_season)
			number_from_csv = int(number_from_csv)
			season_num = int(season_num)

			name = name[1:-1]
			debug_print(name)

			season = find_unique(season_list, lambda season: season.number == season_num, throw_if_not_found=False)
			if season is None:
				debug_print('Adding season %i' % season_num)
				season = Season(number=season_num)
				season_list.append(season)

			if num_in_season != len(season.episodes) + 1:
				raise ValueError('Episode number in season does not match order: expected number %i, row %s' % (
					len(season.episodes) + 1, str(row)))

			if number != number_from_csv:
				raise ValueError('Episode number does not match order: expected number %i, ro %s' % (
					number, str(row)))

			episode = Episode(
				number=number,
				number_in_season=num_in_season,
				season=season,
				name=name)

			episode_list.append(episode)
			season.episodes.append(episode)

	return episode_list, season_list


def parse_connections(filename, db):
	conn_list = []
	with open(filename) as csvFile:
		reader = csv.reader(csvFile)
		for row in reader:
			if row[0].isdigit():

				seas_num, ep_num_in_season, book_num, chap_name, strength, major, notes = row

				seas_num = int(seas_num)
				ep_num_in_season = int(ep_num_in_season)
				book_num = int(book_num)

				if (chap_name == '') or (chap_name == '?'):
					continue

				if strength not in ['0', '1']:
					warn("Chapter strength not 0 or 1: book %i, chapter %s, strength %s" % (book_num, chap_name, strength))
					continue
				strength = int(strength)

				# Make sure chapter name is in the list of chapters!
				chapter = db.find_chapter(chap_name, book_num)

				if not chapter:
					warn("Chapter not found: book %i, chapter %s, notes %s" % (book_num, chap_name, notes))

				season = find_unique(db.seasons, lambda s: s.number == seas_num)
				episode = find_unique(season.episodes, lambda ep: ep.number_in_season == ep_num_in_season)

				connection = Connection(
					episode=episode,
					chapter=chapter,
					strength=strength,
					major=major,
					notes=notes,
				)

				episode.book_connections.append(connection)

	debug_print(repr(conn_list[0:10]))

	return conn_list


def do_parsing(dir='input') -> DB:

	books_filename = os.path.join(dir, 'books.csv')
	chapter_filename = os.path.join(dir, 'chapters.csv')
	combined_filename = os.path.join(dir, 'combined.txt')
	episode_filename = os.path.join(dir, 'episodes.csv')
	connections_filename = os.path.join(dir, 'connections.csv')

	db = DB()

	print("Processing books: %s" % books_filename)
	db.books = parse_books(books_filename)

	print("Processing chapters: %s" % chapter_filename)
	chapter_list = parse_chapters(chapter_filename, db.books)

	print("Processing combined order: %s" % combined_filename)
	combined_book = parse_combined_order(combined_filename, chapter_list, db.books)

	print(len(combined_book.chapters), "chapters in books 4+5")

	db.books.insert(5, combined_book)

	print("")
	print("%i chapters in %i books" % (len(chapter_list), len(db.books)))
	for n, book in enumerate(db.books):
		print("%i: %s" % (n+1, repr(book)))
	print("")

	print("Processing episodes: %s" % episode_filename)
	episodes, db.seasons = parse_episodes(episode_filename)
	print("%i episodes, %i seasons" % (len(episodes), len(db.seasons)))

	print("")

	print("Processing connections: %s" % connections_filename)
	conn_list = parse_connections(connections_filename, db)
	print("%i episode-chapter connections" % len(conn_list))

	return db

