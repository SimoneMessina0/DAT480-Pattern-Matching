
-- A basic AXI Stream register stage without double buffering/skid-buffering

library ieee;
use ieee.std_logic_1164.all;

entity axis_reg is
	generic (
		C_TDATA_WIDTH : integer := 512;
		C_TDEST_WIDTH : integer := 16
	);
	port (
		ap_clk : in std_logic;
    	ap_rst_n : in std_logic;
    	y_tdata : out std_logic_vector (C_TDATA_WIDTH-1 downto 0);
    	y_tvalid : out std_logic;
    	y_tready : in std_logic;
    	y_tkeep : out std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
    	y_tlast : out std_logic;
    	y_tdest : out std_logic_vector (C_TDEST_WIDTH-1 downto 0);
    	x_tdata : in std_logic_vector (C_TDATA_WIDTH-1 downto 0);
    	x_tvalid : in std_logic;
    	x_tready : out std_logic;
    	x_tkeep : in std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
    	x_tlast : in std_logic;
    	x_tdest : in std_logic_vector (C_TDEST_WIDTH-1 downto 0)
	);

end axis_reg;


architecture behavior of axis_reg is

	signal ready : std_logic;
	signal valid : std_logic := '0';
	signal data : std_logic_vector (C_TDATA_WIDTH-1 downto 0);
	signal keep : std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
	signal last : std_logic;
	signal dest : std_logic_vector (C_TDEST_WIDTH-1 downto 0);

begin
	
	ready <= y_tready or not valid;
	x_tready <= ready;

	y_tvalid <= valid;
	y_tdata <= data;
	y_tkeep <= keep;
	y_tlast <= last;
	y_tdest <= dest;

	REG: process(ap_clk, ap_rst_n) begin
		if ap_rst_n /= '1' then
			valid <= '0';
		elsif rising_edge(ap_clk) then
			if (ready and x_tvalid) = '1' then
				valid <= '1';
				keep <= x_tkeep;
				last <= x_tlast;
				dest <= x_tdest;
				for i in 0 to (C_TDATA_WIDTH/8)-1 loop
					if x_tkeep(i) = '1' then
						data((i+1)*8-1 downto i*8) <= x_tdata((i+1)*8-1 downto i*8);
					end if;
				end loop;
			elsif y_tready = '1' then
				valid <= '0';
			end if;
		end if;
	end process;


end behavior;

