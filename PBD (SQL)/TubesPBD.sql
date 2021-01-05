/* 
	CREATE ENTITY
*/

CREATE TABLE mahasiswa (
	nim char(10) PRIMARY KEY,
	first_name_maha varchar(20),
	last_name_maha varchar(20)
);

CREATE TABLE mataKuliah (
	mataKuliahID char(6) PRIMARY KEY,
	namaMataKuliah varchar(50)
);

CREATE TABLE taking (
	nim char(10) FOREIGN KEY (nim) REFERENCES mahasiswa(nim),
	mataKuliahID char(6) FOREIGN KEY REFERENCES mataKuliah(mataKuliahID),
	PRIMARY KEY (nim, mataKuliahID)
);

CREATE TABLE dosen (
	dosenID char(3) PRIMARY KEY,
	first_name_dosen varchar(50),
	last_name_dosen varchar(50),
);

CREATE TABLE teach (
	mataKuliahID char(6) FOREIGN KEY REFERENCES mataKuliah(mataKuliahID),
	dosenID char(3) FOREIGN KEY REFERENCES dosen(dosenID),
	PRIMARY KEY (mataKuliahID, dosenID)
);

CREATE TABLE sumberDaya (
	sumberDayaID char(10) PRIMARY KEY,
	nama_sumber varchar(100),
	deskripsi varchar(100),
	jenis varchar(50),
	tautan varchar(50),
	mataKuliahID char(6) FOREIGN KEY REFERENCES mataKuliah(matakuliahID) 
);

CREATE TABLE aktivitasPembelajaran (
	aktivitasID char(10) PRIMARY KEY,
	namaAktivitas varchar(100),
	deskripsi varchar(100),
	tanggalMulai date,
	tanggalSelesai date,
	mataKuliahID char(6) FOREIGN KEY REFERENCES mataKuliah(mataKuliahID) 
);

CREATE TABLE kuis (
	kuisID char(10) PRIMARY KEY FOREIGN KEY REFERENCES aktivitasPembelajaran(aktivitasID),
	nilaiMaksimum float,
	jumlahAttempt int,
	jumlahSoal int,
	durasi int
);

CREATE TABLE nilaiKuis (
	kuisID char(10) FOREIGN KEY REFERENCES kuis(kuisID),
	nilaiKuis float,
	nim char(10) FOREIGN KEY REFERENCES mahasiswa(nim)
);

CREATE TABLE tugas (
	tugasID char(10) PRIMARY KEY FOREIGN KEY REFERENCES aktivitasPembelajaran(aktivitasID),
	tipePenilaian varchar(100)
);

CREATE TABLE nilaiTugas (
	tugasID char(10) FOREIGN KEY REFERENCES tugas(tugasID),
	nilaiTugas float,
	tanggalPengumpulan date,
	pukulPengumpulan char(5),
	nim char(10) FOREIGN KEY REFERENCES mahasiswa(nim)
);

CREATE TABLE forum (
	forumID char(10) PRIMARY KEY FOREIGN KEY REFERENCES aktivitasPembelajaran(aktivitasID)
);

CREATE TABLE topikDiskusi (
	topikID char(10) PRIMARY KEY,
	forumID char(10) FOREIGN KEY REFERENCES forum(forumID),
	namaTopik varChar(30)
);

CREATE TABLE komentar (
	topikID char(10) FOREIGN KEY REFERENCES topikDiskusi(topikID),
	isiKomentar varchar(1000),
	tanggalSubmit date,
	pukulSubmit char(5),
	nim char(10) FOREIGN KEY REFERENCES mahasiswa(nim)
);

/*
	INSERT DUMMY DATAS (DML)
*/

INSERT INTO mahasiswa (nim, first_name_maha, last_name_maha) 
VALUES 
	('1301190221', 'Vincentius','Arnold'),
	('1301190222', 'Hassan', 'Ananda'),
	('1301190223', 'Naufal', 'Saputra Widoman'),
	('1301190224', 'Bambank', 'Sueman'),
	('1301190225', 'Dengklek', ' '),
	('1301190226', 'Ganesh', 'Ricola'),
	('1301190227', 'Pemangkus', 'jagatraya'),
	('1301190228', 'Paku', 'Bumitra'),
	('1301190229', 'Jebol', 'Pankreas'),
	('1301190230', 'Mama', 'Lemon')
;

INSERT INTO mataKuliah (mataKuliahID, namaMataKuliah)
VALUES
	('CII2G3', 'Teori Peluang'),
	('CII2C2', 'Analisis Kompleksitas Algoritma'),
	('CII1C2', 'Statistika'),
	('CII2E2', 'RPL: Analisis Kebutuhan'),
	('CII2I2', 'Wawasan Global TIK'),
	('CII1J3', 'Pemodelan Basis Data'),
	('CII2A3', 'Organisasi dan Arsitektur Komputer'),
	('CII1I3', 'Sistem Digital'),
	('CII3B4', 'Pemrograman Berorientasi Objek'),
	('CII4D3', 'Bahasa Inggris untuk Karir')
;

INSERT INTO taking (nim, mataKuliahID)
VALUES 
	('1301190221', 'CII2G3'),
	('1301190221', 'CII2C2'),
	('1301190221', 'CII4D3'),
	('1301190221', 'CII1J3'),
	('1301190222', 'CII2A3'),
	('1301190222', 'CII2G3'),
	('1301190223', 'CII1I3'),
	('1301190223', 'CII2A3'),
	('1301190224', 'CII2E2'),
	('1301190224', 'CII2I2'),
	('1301190225', 'CII4D3'),
	('1301190225', 'CII1J3'),
	('1301190227', 'CII2G3'),
	('1301190227', 'CII4D3'),
	('1301190227', 'CII1J3'),
	('1301190227', 'CII3B4'),
	('1301190229', 'CII4D3'),
	('1301190229', 'CII3B4'),
	('1301190230', 'CII2G3'),	
	('1301190230', 'CII3B4')
;

INSERT INTO dosen (dosenID, first_name_dosen, last_name_dosen)
VALUES
	('EDW', 'Erni', 'Dwi Sumaryatie'),
	('SSD', 'Siti', 'Sa''Adah'),
	('ASD', 'Andit', 'Sudirman'),
	('YPR', 'Yudi', 'Priadi'),
	('GAW', 'Gede', 'Agung Ary Wisudiawan'),
	('ADR', 'Andrian', 'Rakhmatsyah'),
	('AJG', 'Aji', 'Gautama Putra'),
	('PDF', 'Panji', 'Dorhen Ferdian'),
	('AMD', 'Ahmad', 'Manjo Derhian'),
	('INT', 'Iktifar', 'Intan')
;

INSERT INTO teach (mataKuliahID, dosenID)
VALUES 
	('CII2G3', 'EDW'),
	('CII2G3', 'ASD'),
	('CII2G3', 'YPR'),
	('CII2C2', 'SSD'),
	('CII2C2', 'GAW'),
	('CII2E2', 'YPR'),
	('CII1C2', 'GAW'),
	('CII1C2', 'AJG'),
	('CII2I2', 'PDF'),
	('CII2I2', 'AMD'),
	('CII1J3', 'INT'),
	('CII1J3', 'ADR'),
	('CII2A3', 'INT'),
	('CII2A3', 'AJG'),
	('CII1I3', 'SSD'),
	('CII1I3', 'EDW'),
	('CII3B4', 'ASD'),
	('CII3B4', 'SSD'),
	('CII4D3', 'YPR'),
	('CII4D3', 'AMD')
;

INSERT INTO sumberDaya (sumberDayaID, nama_sumber, deskripsi, jenis, tautan, mataKuliahID)
VALUES
	('0000000000', 'Tipe Dasar Variabel', 'Penjelasan tipe data dasar dalam pemrograman', 'PowerPoint', 'www.sample1.com', 'CII2G3'),
	('1111111111', 'Pengenalan Basis Data', 'Penjelasan mengenai Basis Data', 'PDF', 'www.sample2.com', 'CII1J3'),
	('2222222222', 'Rantai Markov', 'Penjelasan mengenai pengertian rantai Markov', 'PDF', 'www.sample3.com', 'CII2G3'),
	('3333333333', 'Pengenalan Program R', 'Bahasa pemrogram R untuk statistika', 'PowerPoint', 'www.sample4.com', 'CII1C2'),
	('4444444444', 'Functional Requirenment','Pengertian FR dan cara membuat FR', 'Video', 'www.sample5.com', 'CII2E2'),
	('5555555555', 'Data Science', 'Kegunaan umum Data Science dalam Data Analisis', 'Video', 'www.sample6.com', 'CII2I2'),
	('6666666666', 'K-Map', 'Terlampir PPTX tentang K-Map di bawah ini', 'Power Point', 'www.sample7.com', 'CII1I3'),
	('7777777777', 'SAP-1', 'Penjelasan tentang SAP-1 ada pada link Video di bawah', 'Video', 'www.sample8.com', 'CII2A3'),
	('8888888888', 'Java: Pengenalan', 'Pengenalan dasar tentang bahasa Java', 'PowerPoint', 'www.sample9.com', 'CII3B4'),
	('9999999999', 'Conversation 2', 'Decribes how to respon someone correct and politely', 'PDF', 'www.sample10.com', 'CII4D3')
;

INSERT INTO aktivitasPembelajaran(aktivitasID, namaAktivitas, deskripsi, tanggalMulai, tanggalSelesai, mataKuliahID)
VALUES
	('CII2G3_K01', 'Kuis 1 Teori Peluang', 'Ujian ini meliputi materi rantai markov', '12 AUG 20', '12 AUG 20', 'CII2G3'),
	('CII2G3_K02', 'Kuis 2 Teori Peluang', 'Ujian ini meliputi materi distribusi peubah acak', '12 SEP 20', '12 SEP 20','CII2G3'),
	('CII2C2_K01', 'Kuis 1 AKA', 'Analisis Correctness Prove Rekursif', '10 AUG 20', '10 AUG 20', 'CII2C2'),
	('CII1C2_K01', 'Korelasi 2 variabel', 'Menghitung korelasi antar 2 variabel', '20 AUG 20', '20 AUG 20', 'CII2C2'),
	('CII2I2_K03', 'Membuat histogram', 'Pembuatan histogram dengan program Python', '1 SEP 20', '1 SEP 20', 'CII2I2'),
	('CII2A3_K02', 'SAP-1', 'Membuat instruksi assembly', '2 SEP 20', '2 SEP 20', 'CII2A3'),
	('CII2E2_K02', 'Requirment', 'Kuis 2 RPL', '19 AUG 20', '22 AUG 20', 'CII2E2'),
	('CII1J3_K01', 'Data Base', 'Kuis 1 Database', '7 AUG 20', '7 AUG 20', 'CII1J3'),
	('CII1I3_K01', 'K-Map', 'Kuis 1 SISDIG', '1 AUG 20', '7 AUG 20', 'CII1I3'),
	('CII2I2_K01', 'Penggunaan data science', 'Kuis 1 WGTIK', '9 AUG 20', '9 AUG 20', 'CII2I2'),
	('CII2G3_T01', 'Tugas 1 Teori Peluang', 'Tugas mengenai sample peubah acak', '12 AUG 20', '12 AUG 20', 'CII2G3'),
	('CII2G3_T02', 'Tugas 2 Teori Peluang', 'Tugas Distribusi khusus peubah acak diskrit', '12 SEP 20', '19 SEP 20','CII2G3'),
	('CII1C2_T01', 'Korelasi 1', 'Menghitung korelasi', '10 AUG 20', '17 AUG 20', 'CII1C2'),
	('CII2C2_T01', 'Data Science', 'Kegunaan Data Science', '1 SEP 20', '8 SEP 20', 'CII2I2'),
	('CII2E2_T02', 'Requirment', 'Tugas 2 RPL', '19 AUG 20', '22 AUG 20', 'CII2E2'),
	('CII2I2_T03', 'Data Science', 'Kegunaan Data Science', '1 SEP 20', '9 SEP 20', 'CII2I2'),
	('CII1J3_T01', 'Data Base', 'Tugas 1 Database', '7 AUG 20', '14 AUG 20', 'CII1J3'),
	('CII2A3_T02', 'SAP-2', 'Membuat instruksi assembly', '2 SEP 20', '9 SEP 20', 'CII2A3'),
	('CII1I3_T01', 'K-Map', 'Tugas 1 SISDIG', '1 AUG 20', '7 AUG 20', 'CII1I3'),
	('CII2I2_T02', 'Data Science 2', 'Implementasi Data Science', '1 SEP 20', '8 SEP 20', 'CII2I2'),
	('CII2C2_F01', 'Data Science', 'Kegunaan Data Science', '1 SEP 20', '1 SEP 20', 'CII2I2'),
	('CII2G3_F01', 'Forum 1 Teori Peluang', 'Jika ada pertanyaan, silahkan.', '12 AUG 20', '12 AUG 20', 'CII2G3'),
	('CII1C2_F02', 'Korelasi 1', 'Pertanyaan?', '4 SEP 20', '19 SEP 20', 'CII1C2'),
	('CII2E2_F03', 'Requirement', 'Ada pertanyaan?', '7 SEP 20', '14 SEP 20', 'CII2E2'),
	('CII2I2_F01', 'Data Science', 'Forum wajib di isi', '1 OCT 20', '7 OCT 20', 'CII2I2'),
	('CII1J3_F03', 'Forum 3 PBD', 'Silahkan bertanya', '19 OCT 20', '26 OCT 20', 'CII1J3'),
	('CII2A3_F01', 'Forum 1 COA', 'Apa ada pertanyaan', '3 AUG 20', '10 AUG 20', 'CII2A3'),
	('CII1I3_F01', 'Forum 1 SISDIG', 'Hayo bertanya', '9 AUG 20', '14 AUG 20', 'CII1I3'),
	('CII3B4_F01', 'FORUM 1 PBO', 'Forum mohon diisi', '3 AUG 20', '13 AUG 20', 'CII3B4'),
	('CII4D3_F02', 'Forum 2 ING', 'Any question?', '4 OCT 20', '8 OCT 20', 'CII4D3')
;

INSERT INTO kuis (kuisID, nilaiMaksimum, jumlahAttempt, jumlahSoal, durasi)
VALUES 
	('CII2G3_K01', '100', '1', '20', '120'),
	('CII2G3_K02', '100', '1', '10', '100'),
	('CII2C2_K01', '100', '2', '5', '100'),
	('CII1C2_K01', '100', '1', '25', '120'),
	('CII2I2_K03', '100', '1', '2', '90'),
	('CII2A3_K02', '100', '2', '10', '90'),
	('CII2E2_K02', '120', '2', '5', '100'),
	('CII1J3_K01', '120', '2', '15', '120'),
	('CII1I3_K01', '100', '1', '10', '90'),
	('CII2I2_K01', '100', '1', '2', '90')
;

INSERT INTO tugas (tugasID, tipePenilaian)
VALUES
	('CII2G3_T01', 'Highest Grade'),
	('CII2G3_T02', 'Highest Grade'),
	('CII2C2_T01', 'Highest Grade'),
	('CII1C2_T01', 'Highest Grade'),
	('CII2E2_T02', 'Highest Grade'),
	('CII2I2_T03', 'Highest Grade'),
	('CII1J3_T01', 'Highest Grade'),
	('CII2A3_T02', 'Highest Grade'),
	('CII1I3_T01', 'Highest Grade'),
	('CII2I2_T02', 'Highest Grade')
;

INSERT INTO forum (forumID)
VALUES 
	('CII2G3_F01'),
	('CII2C2_F01'),
	('CII1C2_F02'),
	('CII2E2_F03'),
	('CII2I2_F01'),
	('CII1J3_F03'),
	('CII2A3_F01'),
	('CII1I3_F01'),
	('CII3B4_F01'),
	('CII4D3_F02')
;

INSERT INTO nilaiKuis (kuisID, nim, nilaiKuis)
VALUES
	('CII2G3_K01', '1301190221', '98'),
	('CII2C2_K01', '1301190221', '90'),
	('CII2G3_K01', '1301190222', '89'),
	('CII2G3_K01', '1301190223', '70')
/*	('CII1J3_K01', '1301190225', '111') */
;

INSERT INTO nilaiTugas (tugasID, nim, nilaiTugas, tanggalPengumpulan, pukulPengumpulan)
VALUES
	('CII2G3_T01', '1301190221', '100', '12 AUG 20', '12-39'),
	('CII2G3_T02', '1301190221', '80', '15 AUG 20', '09-13'),
	('CII2G3_T02', '1301190222', '89', '10 SEP 20', '16-12')
/*	('CII1J3_T01', '1301190223', '70', '5 SEP 20', '12=11'),
	('CII2A3_T02', '1301190225', '111', '8 SEP 20', '14-34'),
	('CII2I2_T03', '1301190221', '98', '25 SEP 20', '11-43')
*/
;

INSERT INTO topikDiskusi (topikID, forumID, namaTopik)
VALUES
	('CII2C2_P01', 'CII2C2_F01', 'Pertanyaan?'),
	('CII2G3_P01', 'CII2G3_F01', 'Diskusi pada kolom di bawah')
;

/*
	DML QUERY
*/

UPDATE mahasiswa SET first_name_maha = 'saya coba' WHERE nim = '1301190221';

SELECT * FROM aktivitasPembelajaran, kuis WHERE aktivitasPembelajaran.aktivitasID = kuis.kuisID;
SELECT * FROM mahasiswa, kuis, nilaiKuis WHERE mahasiswa.nim = '1301190221' and nilaiKuis.nim = mahasiswa.nim and nilaiKuis.kuisID = kuis.kuisID;

UPDATE mahasiswa SET first_name_maha = 'Vincentius' WHERE nim = '1301190221';

SELECT * FROM mahasiswa WHERE first_name_maha LIKE 'v%';
SELECT * FROM mahasiswa WHERE first_name_maha LIKE '%a%';

SELECT first_name_maha, mataKuliahID FROM taking, mahasiswa WHERE mahasiswa.nim = taking.nim;

SELECT taking.nim, taking.mataKuliahID, teach.dosenID FROM taking INNER JOIN teach ON taking.mataKuliahID = teach.mataKuliahID WHERE taking.mataKuliahID = teach.mataKuliahID;
SELECT mahasiswa.nim, taking.mataKuliahID FROM mahasiswa LEFT JOIN taking ON taking.nim = mahasiswa.nim;
SELECT dosen.dosenID, teach.mataKuliahID FROM dosen RIGHt JOIN teach ON dosen.dosenID = teach.dosenID;

SELECT taking.nim, mataKuliahID FROM taking, mahasiswa WHERE mahasiswa.nim = (SELECT mahasiswa.nim FROM mahasiswa WHERE first_name_maha = 'vincentius') AND mahasiswa.nim = taking.nim;

DROP TABLE komentar;
DROP TABLE topikDiskusi;
DROP TABLE forum;
DROP TABLE nilaiTugas;
DROP TABLE tugas;
DROP TABLE nilaiKuis;
DROP TABLE kuis;
DROP TABLE aktivitasPembelajaran;
DROP TABLE teach;
DROP TABLE taking;
DROP TABLE sumberdaya;
DROP TABLE mahasiswa;
DROP TABLE mataKuliah;
DROP TABLE dosen;