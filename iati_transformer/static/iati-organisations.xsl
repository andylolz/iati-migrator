<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output indent="yes"/>
    <xsl:template match="iati-organisations">
        <iati-organisations version="2.03">
            <xsl:if test="@generated-datetime"><xsl:attribute name="generated-datetime"><xsl:value-of select="@generated-datetime" /></xsl:attribute></xsl:if>

            <xsl:for-each select="iati-organisation">
                <iati-organisation>
                    <xsl:if test="@last-updated-datetime"><xsl:attribute name="last-updated-datetime"><xsl:value-of select="@last-updated-datetime" /></xsl:attribute></xsl:if>
                    <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                    <xsl:if test="default-currency"><xsl:attribute name="default-currency"><xsl:value-of select="default-currency" /></xsl:attribute></xsl:if>

                    <xsl:for-each select="iati-identifier">
                        <organisation-identifier>
                            <xsl:value-of select="text()" />
                        </organisation-identifier>
                    </xsl:for-each>

                    <xsl:if test="name">
                        <name>
                            <xsl:for-each select="name">
                                <narrative>
                                    <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                                    <xsl:value-of select="text()" />
                                </narrative>
                            </xsl:for-each>
                        </name>
                    </xsl:if>

                    <xsl:if test="reporting-org">
                        <reporting-org>
                            <xsl:if test="reporting-org/@ref"><xsl:attribute name="ref"><xsl:value-of select="reporting-org/@ref" /></xsl:attribute></xsl:if>
                            <xsl:if test="reporting-org/@type"><xsl:attribute name="type"><xsl:value-of select="reporting-org/@type" /></xsl:attribute></xsl:if>
                            <xsl:if test="reporting-org/@secondary-reporter"><xsl:attribute name="secondary-reporter"><xsl:value-of select="reporting-org/@secondary-reporter" /></xsl:attribute></xsl:if>

                            <xsl:for-each select="reporting-org">
                                <narrative>
                                    <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                                    <xsl:value-of select="text()" />
                                </narrative>
                            </xsl:for-each>
                        </reporting-org>
                    </xsl:if>

                    <xsl:for-each select="total-budget">
                        <total-budget>
                            <period-start>
                                <xsl:if test="period-start/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-start/@iso-date" /></xsl:attribute></xsl:if>
                            </period-start>
                            <period-end>
                                <xsl:if test="period-end/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-end/@iso-date" /></xsl:attribute></xsl:if>
                            </period-end>
                            <value>
                                <xsl:if test="value/@currency"><xsl:attribute name="currency"><xsl:value-of select="value/@currency" /></xsl:attribute></xsl:if>
                                <xsl:if test="value/@value-date"><xsl:attribute name="value-date"><xsl:value-of select="value/@value-date" /></xsl:attribute></xsl:if>
                                <xsl:value-of select="value/text()" />
                            </value>
                        </total-budget>
                    </xsl:for-each>

                    <xsl:for-each select="recipient-org-budget">
                        <recipient-org-budget>
                            <recipient-org>
                                <xsl:if test="recipient-org/@ref"><xsl:attribute name="ref"><xsl:value-of select="recipient-org/@ref" /></xsl:attribute></xsl:if>
                                <xsl:for-each select="recipient-org">
                                    <narrative>
                                        <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                                        <xsl:value-of select="text()" />
                                    </narrative>
                                </xsl:for-each>
                            </recipient-org>
                            <period-start>
                                <xsl:if test="period-start/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-start/@iso-date" /></xsl:attribute></xsl:if>
                            </period-start>
                            <period-end>
                                <xsl:if test="period-end/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-end/@iso-date" /></xsl:attribute></xsl:if>
                            </period-end>
                            <value>
                                <xsl:if test="value/@currency"><xsl:attribute name="currency"><xsl:value-of select="value/@currency" /></xsl:attribute></xsl:if>
                                <xsl:if test="value/@value-date"><xsl:attribute name="value-date"><xsl:value-of select="value/@value-date" /></xsl:attribute></xsl:if>
                                <xsl:value-of select="value/text()" />
                            </value>
                        </recipient-org-budget>
                    </xsl:for-each>

                    <xsl:for-each select="recipient-country-budget">
                        <recipient-country-budget>
                            <recipient-country>
                                <xsl:if test="recipient-country/@code"><xsl:attribute name="code"><xsl:value-of select="recipient-country/@code" /></xsl:attribute></xsl:if>
                                <xsl:for-each select="recipient-country">
                                    <narrative>
                                        <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                                        <xsl:value-of select="text()" />
                                    </narrative>
                                </xsl:for-each>
                            </recipient-country>
                            <period-start>
                                <xsl:if test="period-start/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-start/@iso-date" /></xsl:attribute></xsl:if>
                            </period-start>
                            <period-end>
                                <xsl:if test="period-end/@iso-date"><xsl:attribute name="iso-date"><xsl:value-of select="period-end/@iso-date" /></xsl:attribute></xsl:if>
                            </period-end>
                            <value>
                                <xsl:if test="value/@currency"><xsl:attribute name="currency"><xsl:value-of select="value/@currency" /></xsl:attribute></xsl:if>
                                <xsl:if test="value/@value-date"><xsl:attribute name="value-date"><xsl:value-of select="value/@value-date" /></xsl:attribute></xsl:if>
                                <xsl:value-of select="value/text()" />
                            </value>
                        </recipient-country-budget>
                    </xsl:for-each>

                    <xsl:for-each select="document-link">
                        <document-link>
                            <xsl:if test="@url"><xsl:attribute name="url"><xsl:value-of select="@url" /></xsl:attribute></xsl:if>
                            <xsl:if test="@format"><xsl:attribute name="format"><xsl:value-of select="@format" /></xsl:attribute></xsl:if>

                            <xsl:if test="title">
                                <title>
                                    <xsl:for-each select="title">
                                        <narrative>
                                            <xsl:if test="@xml:lang"><xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute></xsl:if>
                                            <xsl:value-of select="text()" />
                                        </narrative>
                                    </xsl:for-each>
                                </title>
                            </xsl:if>
                            <xsl:for-each select="category">
                                <category>
                                    <xsl:if test="@code"><xsl:attribute name="code"><xsl:value-of select="@code" /></xsl:attribute></xsl:if>
                                </category>
                            </xsl:for-each>
                            <xsl:for-each select="language">
                                <language>
                                    <xsl:if test="@code"><xsl:attribute name="code"><xsl:value-of select="@code" /></xsl:attribute></xsl:if>
                                </language>
                            </xsl:for-each>
                        </document-link>
                    </xsl:for-each>
                </iati-organisation>
            </xsl:for-each>
        </iati-organisations>
    </xsl:template>
</xsl:stylesheet>
